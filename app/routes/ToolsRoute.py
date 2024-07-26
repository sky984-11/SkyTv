'''
Description: 
Author: sky
Date: 2024-07-25 16:09:23
LastEditTime: 2024-07-26 08:51:07
LastEditors: sky
'''
from flask import request, jsonify, abort
from db import Video, VodDetail, PlayUrl, db,Source,app
from utils.tools import with_app_context, paginate
from sqlalchemy.orm import joinedload



def check_for_updates():
    """
    app更新推送接口
    app每次打开程序都会调用此接口，发送当前app版本，后端检查是否是最新版本，如果不是则返回更新地址和消息
    """
    SYSTEM_VERSION = {
    "latest_version": "0.5.0",
    "update_url": "https://www.baidu.com"
    }
    client_version = request.args.get('client_version')
    if not client_version:
        return jsonify({"error": "Client version not provided"}), 400
    
    if client_version != SYSTEM_VERSION["latest_version"]:
        return jsonify({"code": 200, "result":{
            "client_version":client_version,
            "update_required": True,
            "is_show": True,
            "latest_version": SYSTEM_VERSION["latest_version"],
            "update_url": SYSTEM_VERSION["update_url"],
        }}), 200
    else:
        return jsonify({"code": 200, "result":{
            "is_show": False,
        }}), 200
