'''
Description: 
Author: sky
Date: 2024-06-25 08:20:37
LastEditTime: 2024-07-04 09:06:21
LastEditors: sky
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy_tv.api import Api
from scrapy_tv.cache import MyCache
from scrapy.utils.project import get_project_settings


class ScrapyTvPipeline:
    def __init__(self):
        self.settings = get_project_settings()
        self.api_url = self.settings['API_SERVER_NAME'] + '/api/' + self.settings['API_VERSION']
        self.api = Api(self.api_url)
        self.chche = cache = MyCache(self.settings['CACHE_PATH'])
    def process_item(self, item, spider):
        print(self.api.api_url)
        return ItemAdapter(item)
