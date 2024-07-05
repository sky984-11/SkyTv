'''
Description: api接口
Author: sky
Date: 2024-07-04 08:36:06
LastEditTime: 2024-07-05 09:07:01
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
            关闭所有热门影视
        """
        return self.get_data_from_server(self.api_url)
    
    def sync_tv(self,data):
        """
            同步影视
        """
        return self.send_data_to_server(data,self.api_url)