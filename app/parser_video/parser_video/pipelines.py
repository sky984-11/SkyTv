'''
Description: 
Author: sky
Date: 2024-07-07 08:38:01
LastEditTime: 2024-07-09 13:40:28
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
        # self.cahce = MultiDBCacheManager()
    def process_item(self, item, spider):
        key = ''.join([item["vod_title"],item["vod_source"],item["vod_episodes"]]) 
        item_dict = dict(item)
        self.api.sync_video(item_dict)
        # video_cache = self.cahce.get("video_cache",''.join([item["vod_title"],item["vod_type"]])) #视频表缓存
        # play_url_cache = self.cahce.get("play_url_cache",key)  #播放表缓存

        # vod_pic_url_hash = hashlib.md5(item['vod_pic_url'].encode('utf-8')).hexdigest() #将会发生变化的值存在缓存中
        # print(key,vod_pic_url_hash)
        # if video_cache is None:
        #     self.api.video_and_vod_detail(item_dict) # 添加到两个表中(video,vod_detail) 添加接口需要先根据key查询判断是否存在，存在则不添加
        #     self.cahce.set("video_cache",  ''.join([item["vod_title"],item["vod_type"]]), vod_pic_url_hash) # 缓存图片链接hash值
        # else:
        #     if vod_pic_url_hash != video_cache: #值发生变化则更新表
        #         main_source = self.api.get_main_sources()
        #         if main_source['name'] == item['vod_source']:   # 只更新主要源的图片即可
        #             video = self.api.get_video_by_title_and_type(item['vod_title'], item['vod_type'])
        #             self.api.update_video(video['id'],item_dict)  # 先查出id，然后根据id进行更新
        #             self.cahce.set("video_cache", ''.join([item["vod_title"],item["vod_type"]]), vod_pic_url_hash)

        # play_url_hash = hashlib.md5(item['play_url'].encode('utf-8')).hexdigest()
        # if play_url_cache is None:
        #     vod_detail = self.api.get_vod_detail_id(item['play_title'], item['play_from'], item['vod_episodes'])  #这里需要先查vod_detail_id
        #     item['vod_detail_id'] = vod_detail['vod_detail_id']
        #     self.api.create_play_url(item_dict)
        #     self.cahce.set("play_url_cache", key, play_url_hash) # 缓存播放链接hash值
        # else:
        #     if play_url_hash != play_url_cache: #值发生变化则更新表
        #         play_url = self.api.get_play_url_by_details(item['play_title'], item['play_from'], item['vod_episodes'])  # 先查出id，然后根据id进行更新
        #         self.api.update_play_url(play_url['id'],item_dict)
        #         self.cahce.set("play_url_cache", key, play_url_hash)
        
        return item
