'''
Description: 
Author: sky
Date: 2024-06-25 08:20:37
LastEditTime: 2024-06-30 18:01:15
LastEditors: sky
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests
import json

SERVER_NAME='http://127.0.0.1:5115'
API_VERSION = '/api/v1'


#  首页每天更新 1.消除表hot为false 2.判断title是否存在表中  3.存在则添加，不存在则修改


class ScrapyTvPipeline:
    def process_item(self, item, spider):
        headers = {'Content-Type': 'application/json'} 
        tv_api_url = SERVER_NAME + API_VERSION + '/tv/add'
        episodes_api_url = SERVER_NAME + API_VERSION + '/episodes/add'
        requests.post(tv_api_url, data=json.dumps(item), headers=headers)  
        requests.post(episodes_api_url, data=json.dumps(item), headers=headers) 
        return item
