'''
Description: 
Author: sky
Date: 2024-07-07 16:10:17
LastEditTime: 2024-07-07 16:15:40
LastEditors: sky
'''
import diskcache

class MultiDBCacheManager:
    """多数据库缓存管理器"""

    def __init__(self, base_cache_path='./cache'):
        self.caches = {}
        self.base_cache_path = base_cache_path

    def get_cache(self, db_name):
        """获取指定数据库的缓存实例"""
        if db_name not in self.caches:
            cache_path = f"{self.base_cache_path}/{db_name}"
            self.caches[db_name] = diskcache.Cache(cache_path)
        return self.caches[db_name]

    def set(self, db_name, key, value):
        """设置指定数据库的缓存"""
        cache = self.get_cache(db_name)
        cache.set(key, value)

    def get(self, db_name, key):
        """获取指定数据库的缓存"""
        cache = self.get_cache(db_name)
        return cache.get(key)

    def top(self, db_name, limit=50):
        """获取指定数据库的部分缓存，默认50条"""
        cache = self.get_cache(db_name)
        all_keys = cache.iterkeys()

        count = 0
        items = {}
        for key in all_keys:
            value = cache.get(key)
            items[key] = value
            count += 1
            if count == int(limit):
                break

        return items