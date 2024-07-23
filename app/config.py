'''
Description: 
Author: sky
Date: 2024-07-06 14:07:50
LastEditTime: 2024-07-23 13:54:41
LastEditors: sky
'''

import os 


basedir = os.path.abspath(os.path.dirname(__file__))  
DATABASE_PATH = os.path.join(basedir, 'SkyTv.db')  

class BaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    static_folder='./static'
 
 
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE_PATH
    # 这里填写自己的服务端地址
    SERVER_NAME='113.31.114.236:5115'
    DEBUG=True

 
class DefaultConfig(BaseConfig):
    API_VERSION='v1'
    