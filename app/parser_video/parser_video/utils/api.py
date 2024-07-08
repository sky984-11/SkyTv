'''
Description: 
Author: sky
Date: 2024-07-07 09:03:33
LastEditTime: 2024-07-08 09:13:25
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

    def get_data_from_server(self, url):
        """
        从服务器获取数据 (GET).
        """
        return self._request('GET', url)

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
    
    def get_main_sources(self):
        """
        获取主要源.
        """
        return self.get_data_from_server('/source/main')
    
    def video_and_vod_detail(self, data):
        """
        添加视频和视频详情.
        """
        return self.send_data_to_server(data, '/video/video_and_vod_detail')
    
    def get_video_by_title_and_type(self, vod_title, vod_type):
        """
        根据标题和类型获取视频.
        """
        return self.get_data_from_server('/video/' + vod_title + '/' + vod_type)
    
    def update_video(self, video_id,data):
        """
        更新视频.
        """
        return self.update_data_on_server(data, '/video/' + video_id)
    
    def create_play_url(self, data):
        """
        添加播放URL.
        """
        return self.send_data_to_server(data, '/play_url')
    
    def get_play_url_by_details(self, play_title, play_from, vod_episodes):
        """
        根据详情获取播放URL.
        """
        return self.get_data_from_server('/play_url/' + play_title + '/' + play_from + '/' + vod_episodes)
    
    def update_play_url(self, play_url_id, data):
        """
        更新播放URL.
        """
        return self.update_data_on_server(data, '/play_url/' + play_url_id)

    # def close_all_hot_tv(self):
    #     """
    #     关闭所有热门影视.
    #     """
    #     return self.delete_data_from_server('/tv/close/hot')

    # def sync_video(self, data):
    #     """
    #     同步视频
    #     """
    #     return self.send_data_to_server(data, '/video')