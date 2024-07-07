'''
Description: 
Author: sky
Date: 2024-07-07 08:38:01
LastEditTime: 2024-07-08 06:51:13
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
        key = ''.join([item["vod_title"],item["vod_source"],item["vod_episodes"]]) 
        
        video_cache = self.cahce.get("video_cache",key) #视频表缓存
        play_url_cache = self.cahce.get("play_url_cache",key)  #播放表缓存
        # vod_detail_cache = self.cahce.get("vod_detail_cache",key) #详情表暂时不加缓存，因为只会新增，不会修改

        vod_pic_url_hash = hashlib.md5(item['vod_pic_url'].encode('utf-8')).hexdigest() #将会发生变化的值存在缓存中
        if video_cache is None:
            # self.api.send_data_to_server(item, "") 添加到两个表中(video,vod_detail) 添加接口需要先根据key查询判断是否存在，存在则不添加
            self.cahce.set("video_cache", key, vod_pic_url_hash) # 缓存图片链接hash值
        else:
            if vod_pic_url_hash != video_cache: #值发生变化则更新表
                # self.api.send_data_to_server(item, "") 更新
                self.cahce.set("video_cache", key, vod_pic_url_hash)

        play_url_hash = hashlib.md5(item['play_url'].encode('utf-8')).hexdigest()
        if play_url_cache is None:
            # self.api.send_data_to_server(item, "") 添加
            self.cahce.set("play_url_cache", key, play_url_hash) # 缓存播放链接hash值
        else:
            if play_url_hash != play_url_cache: #值发生变化则更新表
                # self.api.send_data_to_server(item,"") 更新
                self.cahce.set("play_url_cache", key, play_url_hash)
        
        return item
