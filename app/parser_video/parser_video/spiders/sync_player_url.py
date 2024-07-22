import scrapy
from scrapy.http import Request
from urllib.parse import urlparse
import re
from parser_video.utils.api import Api
from parser_video.items import ParserVideoItem
# from parser_video.utils.cache import MultiDBCacheManager

# 思考：如何减少请求次数(接口请求和网站请求)

class KekeSpider(scrapy.Spider):
    name = "sync_player_url"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = Api()
        self.base_url = None



    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.base_url = spider.api.get_source(spider.name).get('url')
        return spider

    def start_requests(self):
        #title + source + type确定唯一video,后续缓存以此为key存储url
        if self.base_url:
            page = 1
            while True:
                play_urls = self.api.get_all_play_urls(page)
                for item in play_urls:
                    next_url = ''.join([self.base_url,item['play_page']])
                    yield Request(
                        url=next_url,
                        callback=self.parse_player,
                        meta=item
                    )
                page += 1
                if len(play_urls) < 10:
                    break
            

    def extract_play_url(self, html):
        url_pattern = r'src:\s*"([^"]+)"'
        match = re.search(url_pattern, html)
        return match.group(1) if match else ""

    def parse_player(self, response):
        """
        爬取播放界面
        """
        play_url = self.extract_play_url(response.text)
        item = {k: v for k, v in response.meta.items() if k in ParserVideoItem.fields}
        item['play_url'] = play_url
        yield item