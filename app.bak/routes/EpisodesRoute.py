'''
Description: 
Author: sky
Date: 2024-06-26 10:18:05
LastEditTime: 2024-07-02 13:39:24
LastEditors: sky
'''
from flask import request, jsonify
from run import app
from db import Episodes, db

def add_episodes():
    """
        添加影视集数
    """
    json_data = request.get_json()
    tv_title = json_data.get("tv_title")
    episode = json_data.get("episode")
    source = json_data.get("source")
    link = json_data.get("link")
    index = json_data.get("index")

    if not episode:
        return jsonify({"code": 400, "msg": "集数不能为空"}), 400

    with app.app_context():
        existing_name = Episodes.query.filter_by(tv_title=tv_title,episode=episode).first()
        if existing_name:
            return jsonify({"code": 401, "msg": "名称已存在,请勿重复添加"}), 401
        new_data = Episodes(tv_title=tv_title, episode=episode, source=source, link=link,index=index)
        db.session.add(new_data)
        db.session.commit()
        return jsonify({"code": 200, "msg": "添加成功"})
 
    

def list_episodes():
    """
        查看某个影视的所有集数
    """
    json_data = request.get_json()
    tv_title = json_data.get("tv_title")

    with app.app_context():
        episodes = db.session.query(Episodes).filter_by(tv_title=tv_title).all()
        data = [item.to_dict() for item in episodes]
        return jsonify({"code": 200, "result": data})
    
