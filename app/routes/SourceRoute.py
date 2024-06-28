from flask import request, jsonify
from run import app
from db import Source, db




def add_source():
    """
        添加来源
        name:网站名称
        url:网站首页地址
    """
    json_data = request.get_json()
    name = json_data.get("name")
    url = json_data.get("url")

    if not name or not url:
        return jsonify({"code": 400, "msg": "网站名称和地址不能为空"}), 400

    with app.app_context():
        existing_name = Source.query.filter_by(name=name).first()
        if existing_name:
            return jsonify({"code": 401, "msg": "网站名称已存在,请勿重复添加"}), 401
        new_data = Source(name=name, url=url)
        db.session.add(new_data)
        db.session.commit()
        app.logger.info(f'{name} {url} 添加成功') 
        return jsonify({"code": 200, "msg": "添加成功"})
    
def del_source_by_id(id):
    """
        删除来源(根据id)
    """
    with app.app_context():
        try:
            source = Source.query.filter_by(id=id).first()
            db.session.delete(source)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": str(e)}), 500

        return jsonify({"code": 200, "msg": f"删除成功"})
    
def del_source_by_name(name):
    """
        删除来源(根据名称)
    """
    with app.app_context():
        try:
            source = Source.query.filter_by(name=name).first()
            db.session.delete(source)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": str(e)}), 500

        return jsonify({"code": 200, "msg": f"删除成功"})
    
def edit_source_url():
    """
        修改来源地址
    """
    json_data = request.get_json()
    with app.app_context():
        try:

            url = json_data.get('url')
            name = json_data.get('name')
            id = json_data.get('id')

            if name:
                source = Source.query.filter_by(name=name).first()
            else:
                source = Source.query.filter_by(id=id).first()

            source.url = url
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": str(e)}), 500

        return jsonify({"code": 200, "msg": '修改成功'})
    
def edit_source_main():
    """
        设置主要来源
    """
    json_data = request.get_json()
    with app.app_context():

        try:
            main = json_data.get('main')
            name = json_data.get('name')
            id = json_data.get('id')
            
            # 首先重置所有Source的main为False
            Source.query.update({'main': False})
            db.session.commit() 

            if name:
                source = Source.query.filter_by(name=name).first()
            else:
                source = Source.query.filter_by(id=id).first()
              
            source.main = main
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": str(e)}), 500

        return jsonify({"code": 200, "msg": '修改成功'})
    
def edit_source_disable():
    """
        是否禁用来源
    """
    json_data = request.get_json()
    with app.app_context():

        try:
            disable = json_data.get('disable')
            name = json_data.get('name')
            id = json_data.get('id')

            if name:
                source = Source.query.filter_by(name=name).first()
            else:
                source = Source.query.filter_by(id=id).first()
              
            source.disable = disable
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": str(e)}), 500

        return jsonify({"code": 200, "msg": '修改成功'})
    
def edit_source_ping():
    """
        是否ping通来源
    """
    json_data = request.get_json()
    with app.app_context():

        try:
            ping = json_data.get('ping')
            name = json_data.get('name')
            id = json_data.get('id')

            if name:
                source = Source.query.filter_by(name=name).first()
            else:
                source = Source.query.filter_by(id=id).first()
              
            source.ping = ping
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": str(e)}), 500

        return jsonify({"code": 200, "msg": '修改成功'})
    
def list_source():
    """
        来源列表
    """
    with app.app_context():
        source = db.session.query(Source).all()

        data = [item.to_dict() for item in source]
        return jsonify({"code": 200, "msg": data})