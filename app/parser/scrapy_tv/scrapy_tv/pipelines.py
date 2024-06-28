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





class ScrapyTvPipeline:
    def process_item(self, item, spider):
        headers = {'Content-Type': 'application/json'} 
        tv_api_url = SERVER_NAME + API_VERSION + '/tv/add'
        episodes_api_url = SERVER_NAME + API_VERSION + '/episodes/add'
        response1 = requests.post(tv_api_url, data=json.dumps(item), headers=headers)  
        response2 = requests.post(episodes_api_url, data=json.dumps(item), headers=headers) 
        print(response1.text,response2.text)
        return item
