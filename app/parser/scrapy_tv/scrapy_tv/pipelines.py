'''
Description: 
Author: sky
Date: 2024-06-25 08:20:37
LastEditTime: 2024-07-05 09:03:52
LastEditors: sky
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import hashlib
import json
from scrapy_tv.api import Api
from scrapy_tv.cache import MyCache
from scrapy.utils.project import get_project_settings


class ScrapyTvPipeline:
    def __init__(self):
        self.settings = get_project_settings()
        self.api_url = self.settings['API_SERVER_NAME'] + '/api/' + self.settings['API_VERSION']
        self.api = Api(self.api_url)
        self.chche = MyCache(self.settings['CACHE_PATH'])
    def process_item(self, item, spider):
        print(self.api.api_url)
        data = ItemAdapter(item)
        key = data['title'] + data['episode']
        serialized_data = json.dumps(item, sort_keys=True)
        item_hash = hashlib.md5(serialized_data.encode('utf-8')).hexdigest()
        if self.chche.get(key) != item_hash: # 缓存不存在需要添加或者更新数据
            self.chche.set(key, item_hash) # 设置缓存
            self.api.close_all_hot_tv()  # 清除热播
            # self.api.sync_tv(data) # 同步
        return ItemAdapter(item)
