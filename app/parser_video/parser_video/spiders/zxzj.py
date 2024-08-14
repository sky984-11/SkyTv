import scrapy
from scrapy.http import Request
from urllib.parse import urlparse
import re
from parser_video.utils.api import Api
from parser_video.utils.tools import read_white_list
from parser_video.items import ParserVideoItem
# from parser_video.utils.cache import MultiDBCacheManager

# 思考：如何减少请求次数(接口请求和网站请求)

class ZxzjSpider(scrapy.Spider):
    name = "zxzj"
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
        # spider.base_url = 'https://www.zxzj.pro'
        return spider

    def start_requests(self):
        # 1:电影，2,3,4,5剧集，6动漫
        # 每页12个，不足12则为最后一页
        # ,2,3,4,5,6
        type_list = [1]
        if self.base_url:
            for type_num in type_list:
                start_url = f'/list/{type_num}-1.html'
                yield Request(
                    url=''.join([self.base_url,start_url.format(type_num=type_num)]),
                    callback=self.parse_page,
                    meta= {
                        "vod_type" : '电影' if type_num == 1 else '动漫' if type_num == 6 else '剧集'
                    }
                )
    def get_next_page_number(self, current_number): 
	        # 假设页码是整数，并且从2开始（因为已经有一个3-2的页面了）  
            current_number = int(current_number.split('-')[-1])  
            return current_number + 1  
  
    def get_next_page_url(self, current_url):  
        # 提取页码部分并递增  
        page_match = current_url.rsplit('-', 1)[-1].rsplit('.', 1)[0]  # 提取'3-2'这样的页码  
        next_page_number = self.get_next_page_number(page_match)  
        # 构造新的URL  
        base_url = current_url.rsplit(page_match, 1)[0]  # 去掉页码部分  
        return f"{base_url}{next_page_number}.html"
    def extract_play_url(self, html):
        url_pattern = r'src:\s*"([^"]+)"'
        match = re.search(url_pattern, html)
        return match.group(1) if match else ""

    def parse_page(self, response):
        """
            分页处理
        """
        try:
            video_list = response.css('div.stui-vodlist__box')
            video_page_total = len(video_list)

            for video in video_list:
                detail_page_url = ''.join([self.base_url,video.css('a.stui-vodlist__thumb::attr(href)').get()])
                
                yield Request(
                    url=detail_page_url,
                    callback=self.parse_video,
                    meta= {
                        "vod_title": video.css('h4.title a::attr(title)').get(),
                        "vod_pic_url": video.css('a.stui-vodlist__thumb::attr(data-original)').get(),
                        "vod_total_episodes": video.css('a.stui-vodlist__thumb span::text').get()
                    }
                )

            if video_page_total == 12:
                yield Request(
                    url=self.get_next_page_url(response.url),
                    callback=self.parse_page,
                    meta=response.meta
                )
        except Exception as e:
            print(f"Error while parsing response for URL: {response.url}. Error: {e}")
            # 可以在这里添加重试机制，例如使用 response.request.meta['retry_times'] 来控制重试次数


    def parse_video(self, response):
        """
        爬取视频详情
        """
        vod_tag = response.css('div.stui-content__detail p.data::text').get()
        vod_content = response.css('span.detail-content::text').get()
        play_url = ''.join([self.base_url,response.css('div.play-btn a::attr(href)').get()])
        yield Request(
                    url=play_url,
                    callback=self.parse_player,
                    meta={
                        "vod_tag":vod_tag,
                        "vod_content":vod_content,
                        "play_page":play_url
                    }
                )

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