'''
Description: 
Author: sky
Date: 2024-07-07 08:38:01
LastEditTime: 2024-07-07 17:24:06
LastEditors: sky
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
from parser_video.utils.api import Api
from parser_video.utils.cache import MultiDBCacheManager


class ParserVideoPipeline:
    def __init__(self):
        self.api = Api()
        self.cahce = MultiDBCacheManager()
    def process_item(self, item, spider):
        vod_key = item["vod_title"] + item["vod_source"] + item["vod_episodes"]
        vod_pic_url_cache = self.cahce.get("video_cache", vod_key)  
        vod_pic_url_hash = hashlib.md5(item['vod_pic_url']).hexdigest()
        if vod_pic_url_cache is None:
            # self.api.send_data_to_server(item, "") 添加
            self.cahce.set("video_cache", vod_key, vod_pic_url_hash) # 缓存图片链接hash值
        else:
            if vod_pic_url_cache != vod_pic_url_hash:
                # self.api.update_data_on_server(item, "") 更新
                self.cahce.set("video_cache", vod_key, vod_pic_url_hash)

        play_url_aes_cache = self.cahce.get("play_url_cache", vod_key)
        play_url_aes_hash = hashlib.md5(item['play_url_aes']).hexdigest()
        if play_url_aes_cache is None:
            # self.api.send_data_to_server(item, "") 添加
            self.cahce.set("play_url_cache", vod_key, play_url_aes_hash) # 缓存播放链接hash值
        else:
            if play_url_aes_cache != play_url_aes_hash:
                # self.api.update_data_on_server(item, "") 更新
                self.cahce.set("play_url_cache", vod_key, play_url_aes_hash)

        collect_url_cache = self.cahce.get("collect_url_cache", vod_key)
        collect_url_hash = hashlib.md5(item['collect_url']).hexdigest()
        if collect_url_cache is None:
            # self.api.send_data_to_server(item, "") 添加
            self.cahce.set("collect_url_cache", vod_key, collect_url_cache) # 缓存采集链接
        else:
            if hashlib.md5(collect_url_cache).hexdigest() != collect_url_hash:
                # self.api.update_data_on_server(item, "") 更新
                self.cahce.set("collect_url_cache", vod_key, collect_url_cache)      
        return item
