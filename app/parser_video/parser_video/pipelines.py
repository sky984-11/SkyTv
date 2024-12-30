'''
Description: 
Author: sky
Date: 2024-07-07 08:38:01
LastEditTime: 2024-07-23 10:29:12
LastEditors: sky
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from parser_video.utils.api import Api
from parser_video.utils.cache import MultiDBCacheManager

class ParserVideoPipeline:
    def __init__(self):
        self.api = Api()
        # self.cahce = MultiDBCacheManager()
    def process_item(self, item, spider):
        item_dict = dict(item)
        if spider.name == 'keke':
            self.api.sync_video(item_dict)
        elif spider.name == 'sync_player_url':   #同步播放地址
            self.api.update_play_url(item_dict['id'],item_dict)
        return item
