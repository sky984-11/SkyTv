'''
Description: keke影视爬取
Author: sky
Date: 2024-07-07 08:42:01
LastEditTime: 2024-07-07 09:10:01
LastEditors: sky
'''
import scrapy  
from scrapy.http import Request
from urllib.parse import urlparse    
import re
from scrapy.utils.project import get_project_settings

  
class KekeSpider(scrapy.Spider):  

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(KekeSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.base_url = get_project_settings().get('KEKE_BASE_URL')
        return spider
    
    name = "keke_home"  
    _blacklist_cache = None

    def start_requests(self):
        '''起始url地址'''
        start_url = self.base_url
        yield scrapy.Request(url=start_url, callback=self.parse)

    def image_base_url(self, response):
        '''从首页获取图片的base_url'''
        user_image_url = response.xpath('/html/body/div[1]/div[3]/div[1]/div[5]/a/img/@src').get()
        parsed_url = urlparse(user_image_url)  
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}" 
        return base_url
    
    def parse(self, response):
        """
        解析响应，提取数据并生成新的请求。
        """

        item = ParserVideoItem()
        item['vod_title'] = response.css('h1.title::text').get()
        item['vod_pic_url'] = response.css('img.poster::attr(src)').get()
        # 填充其他字段...
        yield item