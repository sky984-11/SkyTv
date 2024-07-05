'''
Description: 
Author: sky
Date: 2024-06-25 08:20:37
LastEditTime: 2024-07-05 16:24:09
LastEditors: sky
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
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
        self.cache = MyCache(self.settings['CACHE_PATH'])
        self.hot_tv_cleared = False  # 新增标志变量

    def process_item(self, item, spider):
        key = item['title'] + item['episode']+ item['source']
        serialized_data = item['image'] + item['total_episodes'] + str(item['hot']) + item['link'] 
        item_hash = hashlib.md5(serialized_data.encode('utf-8')).hexdigest()
        
        if self.cache.get(key) != item_hash:  # 缓存不存在需要添加或更新数据
            self.cache.set(key, item_hash)  # 设置缓存
            
            # 确保清除热播操作只执行一次
            if not self.hot_tv_cleared:
                self.api.close_all_hot_tv()  # 清除热播
                self.hot_tv_cleared = True  # 设置标志为已执行
        
            self.api.sync_tv(item)  # 同步
