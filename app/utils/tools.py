'''
Description: 
Author: liupeng
Date: 2025-01-17 08:43:18
LastEditTime: 2025-01-17 10:33:42
LastEditors: liupeng
'''

from functools import wraps
from run import app
from flask import abort,jsonify
# 装饰器，用于自动处理app上下文
def with_app_context(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with app.app_context():
            return func(*args, **kwargs)
    return wrapper

# 分页辅助函数
def paginate(query, page, per_page=10):
    count = query.count()
    pages = (count + per_page - 1) // per_page  # 计算总页数
    if page > pages or page < 1:  # 如果页码超出范围，返回404
        abort(404)
    start = (page - 1) * per_page
    end = start + per_page
    return query[start:end], pages


def make_response(code, msg, data=None):
    return jsonify({"code": code, "msg": msg, "data": data}), code