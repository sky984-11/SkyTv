'''
Description: 
Author: liupeng
Date: 2025-01-16 17:47:07
LastEditTime: 2025-01-17 10:00:25
LastEditors: liupeng
'''

class BaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    # 静态文件目录
    static_folder='./static'
    # api接口版本
    API_VERSION="v1"
    # 默认服务端地址
    SERVER_NAME = "127.0.0.1:5000"
    # JWT 配置
    SECRET_KEY = "super-secret-key"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRE_MINUTES = 60 * 24
 
 
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///./app.db"
    DEBUG=False

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///./app.db"  # 开发环境使用不同的 SQLite 数据库
    # 允许调试信息显示
    DEBUG = True
    # 启用 SQLAlchemy 的自动提交
    SQLALCHEMY_ECHO = True  # 输出 SQL 查询语句，便于调试

