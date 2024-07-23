'''
Description: 
Author: sky
Date: 2024-07-07 09:03:33
LastEditTime: 2024-07-23 10:28:11
LastEditors: sky
'''
import requests
from requests.exceptions import RequestException
from scrapy.utils.project import get_project_settings

class Api:
    def __init__(self):
        self.api_url = get_project_settings().get('API_BASE_SERVER')
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.retry_count = 3

    def _request(self, method, url, data=None, params=None):
        """
        发起网络请求的通用方法。
        :param method: 请求方法 ('GET', 'POST', 'PUT', 'DELETE', etc.)
        :param url: API的相对URL
        :param data: POST或PUT请求的数据
        :param params: GET请求的参数
        :return: JSON响应
        """
        for attempt in range(self.retry_count):
            try:
                response = requests.request(method, self.api_url + url, headers=self.headers, json=data, params=params)
                response.raise_for_status()
                return response.json()
            except RequestException as e:
                print(f"Request failed: {e}")
                if attempt < self.retry_count - 1:
                    continue
                raise

    def send_data_to_server(self, data, url):
        """
        发送数据到服务器 (POST).
        """
        return self._request('POST', url, data=data)

    def get_data_from_server(self, url,params=None):
        """
        从服务器获取数据 (GET).
        """
        return self._request('GET', url,params)

    def update_data_on_server(self, data, url):
        """
        更新服务器上的数据 (PUT).
        """
        return self._request('PUT', url, data=data)

    def delete_data_from_server(self, url):
        """
        从服务器删除数据 (DELETE).
        """
        return self._request('DELETE', url)
    
    def get_source(self, source_name):
        """
        根据名称获取源.
        """
        return self.get_data_from_server('/source/' + source_name)
    
    def get_all_play_urls(self, page):
        """
        获取所有播放链接记录
        """
        params = {'page': page}
        return self.get_data_from_server('/play_url',params=params)
    
    def update_play_url(self, play_url_id, data):
        """
        更新播放链接记录
        """
        return self.update_data_on_server(data, '/play_url/' + str(play_url_id))
        

    def sync_video(self,data):
        """
        同步视频.
        """
        return self.send_data_to_server(data,'/video/sync')