'''
Description: 
Author: sky
Date: 2024-06-28 17:48:34
LastEditTime: 2024-06-28 17:51:28
LastEditors: sky
'''
import requests  
from run import app
  
def check_url_validity(url):  
    try:  
        response = requests.get(url, timeout=5)  # 设置请求超时时间  
        if response.status_code == 200:  # 检查 HTTP 状态码是否为 200  
            # 在这里，你可以进一步解析响应内容、验证签名和时间戳等  
            # 应用额外的业务逻辑...  
            return True  
        else:  
            app.logger.warning(f"URL {url} 无效，HTTP 状态码为:{response.status_code}")  
            return False  
    except requests.exceptions.RequestException as e:  
        app.logger.warning("请求失败:", str(e))  
        return False  
  
url = "https://172.80.104.78:11300/vods/hls/dhz/15/14609/24050319/704150/1280/index.m3u8?appId=kkdy&sign=f6a1bd5d2917c2b36ea0f21cfa5e3ca8&timestamp=1719379666"  
check_url_validity(url)