'''
Description: 
Author: sky
Date: 2024-06-25 08:20:37
LastEditTime: 2024-07-02 15:43:41
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
API_SYNC_URL = SERVER_NAME + API_VERSION + '/tv/sync'
API_DEL_URL = SERVER_NAME + API_VERSION + '/tv/del/all'


class ScrapyTvPipeline:
    def __init__(self):
        # 引入一个类属性来标记删除操作是否已经执行
        self.delete_executed = False
    def process_item(self, item, spider):
        # print(self.delete_executed )
        # return {item['index'],item['title']}

        # 数据删除操作仅在首次执行
        if not self.delete_executed:
            try:
                self.delete_all_data()
                self.delete_executed = True  # 设置标志表示删除操作已完成
            except Exception as e:
                print(f"Error while sending data to delete API: {e}")

        # 确保数据同步操作始终执行
        self.send_data_to_server(item, API_SYNC_URL)
    def send_data_to_server(self, item, url):
        """
        发送数据到服务器
        """
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(item)
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response
    
    def delete_all_data(self):
        """
        删除所有数据
        """
        response = requests.delete(API_DEL_URL)
        response.raise_for_status() 