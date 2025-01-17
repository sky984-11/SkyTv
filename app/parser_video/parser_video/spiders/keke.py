import scrapy
from scrapy.http import Request
from urllib.parse import urlparse
import re
from parser_video.utils.api import Api
from parser_video.utils.tools import read_white_list
from parser_video.items import ParserVideoItem
# from parser_video.utils.cache import MultiDBCacheManager

# 思考：如何减少请求次数(接口请求和网站请求)

class KekeSpider(scrapy.Spider):
    name = "keke"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = Api()
        self.base_url = None
        self.white_list = read_white_list()
        # self.cahce = MultiDBCacheManager()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.base_url = spider.api.get_source(spider.name).get('url')
        return spider

    def start_requests(self):
        #title + source + type确定唯一video,后续缓存以此为key存储url
        if self.base_url:
            for item in self.white_list:
                search_url = f"{self.base_url}/search?os=pc&k={item[0]}"
                yield Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"vod_title": item[0],"vod_type": item[1]}
                )

    def extract_play_url(self, html):
        url_pattern = r'src:\s*"([^"]+)"'
        match = re.search(url_pattern, html)
        return match.group(1) if match else ""

    def parse(self, response):
        try:
            vod_title = response.meta['vod_title']
            vod_type = response.meta['vod_type']
            video_list = response.css('a.search-result-item')
            for video in video_list:
                title_text = video.css('.title::text').get()
                type_text = video.css('.search-result-item-header div::text').get()
                if title_text == vod_title and type_text == vod_type:
                    user_image_url = response.xpath('/html/body/div[1]/div[3]/div[1]/div[5]/a/img/@src').get()
                    parsed_url = urlparse(user_image_url)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    next_url = ''.join([self.base_url,video.css('.search-result-item::attr(href)').get()])
 
                    yield Request(
                    url=next_url,
                    callback=self.parse_episodes,
                    meta={
                        "vod_title": vod_title,
                        "vod_pic_url": ''.join([base_url,video.css('img::attr(data-original)').get()]),
                        "vod_type":vod_type,
                        "vod_tag":'/'.join(video.css('.tags span::text').getall()),
                        "vod_content":video.css('.desc::text').get()
                    }
                )
        except Exception as e:
            print(f"Error while parsing response for URL: {response.url}. Error: {e}")
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
            vod_episodes = data.xpath('text()').get()
            response.meta['vod_episodes'] = vod_episodes
            response.meta['vod_episodes_index'] = vod_episodes_index
            url_href = data.xpath('@href').get()
            response.meta['play_page'] = url_href  # 存储爬取播放地址界面
            next_url = ''.join([self.base_url,url_href])

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
        valid_meta = {k: v for k, v in response.meta.items() if k in ParserVideoItem.fields}
        item = ParserVideoItem(**valid_meta)
        item['play_url'] = play_url
        item['play_status'] = True
        item['play_from'] = self.name     
        yield item