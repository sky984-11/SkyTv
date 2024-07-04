'''
Description: api接口
Author: sky
Date: 2024-07-04 08:36:06
LastEditTime: 2024-07-04 09:04:46
LastEditors: sky
'''
import requests


class Api:
    def __init__(self,api_url):
        self.api_url = api_url
        self.headers = {
            'Content-Type': 'application/json'
        }

    def send_data_to_server(self, data, url):
        """
            发送数据到服务器
            :param data: 数据
            :param url: url
        """
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def get_data_from_server(self, url):
        """
            从服务器获取数据
            :param url: url
        """
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def close_all_hot_tv(self):
        """
            关闭所有热门电视剧
        """
        return self.get_data_from_server(self.api_url)