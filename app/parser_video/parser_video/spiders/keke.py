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
                    dont_filter=True,
                    meta={"vod_title": title}
                )

    def parse(self, response):
        try:
            vod_title = response.meta['vod_title']
            video_list_div = response.css('a.search-result-item')
            for video in video_list_div:
                title_text = video.css('.title::text').get()
                if title_text == vod_title:
                    item = ParserVideoItem()
                    # 直接在 parse 方法中获取图片的 base_url
                    user_image_url = response.xpath('/html/body/div[1]/div[3]/div[1]/div[5]/a/img/@src').get()
                    parsed_url = urlparse(user_image_url)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    item['vod_pic_url'] = base_url + video.css('img::attr(data-original)').get()
                    item['vod_title'] = vod_title
                    item['vod_type'] = video.css('.search-result-item-header div::text').get()
                    item['vod_tag'] = '/'.join(video.css('.tags span::text').getall())
                    item['vod_content'] = video.css('.desc::text').get()
                    yield item
        except Exception as e:
            self.logger.error(f"Error while parsing response for URL: {response.url}. Error: {e}")
            # 可以在这里添加重试机制，例如使用 response.request.meta['retry_times'] 来控制重试次数

    def closed(self, reason):
        self.logger.info("Spider closed, reason: %s", reason)