import scrapy
from scrapy.http import Request
from urllib.parse import urlparse
import re
from parser_video.utils.api import Api
from parser_video.utils.tools import read_white_list
from parser_video.items import ParserVideoItem

class KekeSpider(scrapy.Spider):
    name = "keke"
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = Api()
        self.base_url = None
        self.white_list = read_white_list()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.base_url = spider.api.get_source(spider.name).get('url')
        return spider

    def start_requests(self):
        if self.base_url:
            for title in self.white_list:
                search_url = f"{self.base_url}/search?os=pc&k={title}"
                yield Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"vod_title": title}
                )

    def extract_play_url(self, html):
        url_pattern = r'src:\s*"([^"]+)"'
        match = re.search(url_pattern, html)
        return match.group(1) if match else ""

    def parse(self, response):
        try:
            vod_title = response.meta['vod_title']
            video_list = response.css('a.search-result-item')
            for video in video_list:
                title_text = video.css('.title::text').get()
                if title_text == vod_title:
                    user_image_url = response.xpath('/html/body/div[1]/div[3]/div[1]/div[5]/a/img/@src').get()
                    parsed_url = urlparse(user_image_url)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    next_url = self.base_url + video.css('.search-result-item::attr(href)').get()
 
                    yield Request(
                    url=next_url,
                    callback=self.parse_episodes,
                    meta={
                        "vod_title": vod_title,
                        "vod_pic_url": base_url + video.css('img::attr(data-original)').get(),
                        "vod_type":video.css('.search-result-item-header div::text').get(),
                        "vod_tag":'/'.join(video.css('.tags span::text').getall()),
                        "vod_content":video.css('.desc::text').get()
                    }
                )
        except Exception as e:
            self.logger.error(f"Error while parsing response for URL: {response.url}. Error: {e}")
            # 可以在这里添加重试机制，例如使用 response.request.meta['retry_times'] 来控制重试次数

    def parse_episodes(self,response):
        """
        爬取集数
        """
        vod_total_episodes = response.xpath(
            '/html/body/div[1]/div[3]/div[2]/div[2]/div[3]/div[6]/div[2]/text()').extract_first()
        response.meta['vod_total_episodes'] = vod_total_episodes

        episode_list_div= response.xpath('/html/body/div[1]/div[3]/div[2]/div[4]/div[2]/div[1]/a')
        vod_episodes_index = 1
        for data in episode_list_div: 
            next_url = self.base_url + data.xpath('@href').get()

            vod_episodes = data.xpath('text()').get()
            
            response.meta['vod_episodes'] = vod_episodes
            response.meta['vod_episodes_index'] = vod_episodes_index

            yield Request(
                    url=next_url,
                    callback=self.parse_player,
                    meta=response.meta
                )
            vod_episodes_index += 1 
        
    def parse_player(self, response):
        """
        爬取播放界面
        """
        play_url = self.extract_play_url(response.text)
        item = ParserVideoItem(**response.meta)
        item['play_url'] = play_url
        item['play_status'] = True
        item['play_from'] = self.name
        item['vod_source'] = self.name
        item['vod_score'] = ""
        item['play_title'] = response.meta['vod_title']
        yield item