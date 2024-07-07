import scrapy
from scrapy.http import Request
from urllib.parse import urlparse
import re
from parser_video.utils.api import Api
from parser_video.items import ParserVideoItem

class KekeSpider(scrapy.Spider):
    name = "keke"
    custom_settings = {
        'ROBOTSTXT_OBEY': False,  # 可选，根据项目需求决定是否遵守robots.txt
        'DOWNLOAD_DELAY': 1,      # 可选，下载延迟，防止被封IP
    }

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
        if self.base_url:
            yield Request(url=self.base_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        """
        解析响应，提取数据并生成新的请求。
        """
        try:
            item = ParserVideoItem()
            item['vod_title'] = response.css('h1.title::text').get()
            item['vod_pic_url'] = response.css('img.poster::attr(src)').get()
            yield item
        except Exception as e:
            self.logger.error(f"Error parsing response: {e}")

    def closed(self, reason):
        """
        爬虫关闭时的回调，可用于释放资源。
        """
        # 在这里关闭API客户端，释放资源等
        pass