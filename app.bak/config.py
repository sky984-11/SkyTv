"""
@ Date: 2024-04-26 15:31:44
@ LastEditors: sky
@ LastEditTime: 2024-05-08 10:11:11
@ FilePath: /SkyTunnel/app/config.py
@ Desc: 
"""
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
    SERVER_NAME='127.0.0.1:5115'
    DEBUG=True

 
class DefaultConfig(BaseConfig):
    API_VERSION='v1'
    