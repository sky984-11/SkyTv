'''
Description: 
Author: sky
Date: 2024-07-07 08:38:01
LastEditTime: 2024-07-07 08:49:33
LastEditors: sky
'''
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserVideoItem(scrapy.Item):
    # define the fields for your item here like:
    vod_title = scrapy.Field()
    vod_type = scrapy.Field()
    vod_score = scrapy.Field()
    vod_pic_url = scrapy.Field()
    vod_content = scrapy.Field()
    vod_tag = scrapy.Field()
    vod_source = scrapy.Field()
    vod_episodes = scrapy.Field()
    vod_episodes_index = scrapy.Field()
    play_title = scrapy.Field()
    play_from = scrapy.Field()
    play_status = scrapy.Field()
    play_url = scrapy.Field()
