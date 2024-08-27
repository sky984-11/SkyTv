'''
Description: 缓存管理器
Author: sky
Date: 2024-07-04 08:59:08
LastEditTime: 2024-07-04 09:00:10
LastEditors: sky
'''
import diskcache

class MyCache:
    """缓存管理器"""

    def __init__(self, cache_path):
        self.cache = diskcache.Cache(cache_path)

    def set(self, key, value):
        """设置缓存"""
        self.cache.set(key, value)

    def get(self, key):
        """获取缓存"""
        return self.cache.get(key)
    
    def top(self, limit=50):
        """获取部分缓存,默认50条"""
        # 获取所有缓存项的键
        all_keys = self.cache.iterkeys()

        # 用于计数的变量和保存结果的字典
        count = 0
        items = {}
        for key in all_keys:
            value = self.cache.get(key)
            items[key] = value
            count += 1
            if count == int(limit):
                break

        return items