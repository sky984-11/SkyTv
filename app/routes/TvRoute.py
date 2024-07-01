from flask import request, jsonify
from run import app
from db import Tv,Episodes, db

def add_tv():
    """
        添加影视
    """
    json_data = request.get_json()
    title = json_data.get("title")
    image = json_data.get("image")
    source = json_data.get("source")
    description = json_data.get("description")
    total_episodes = json_data.get("total_episodes")
    rating = json_data.get("rating")
    type = json_data.get("type")
    hot = json_data.get("hot")
    tags = json_data.get("tags")

    if not title:
        return jsonify({"code": 400, "msg": "名称不能为空"}), 400

    with app.app_context():
        existing_name = Tv.query.filter_by(title=title).first()
        if existing_name:
            return jsonify({"code": 401, "msg": "名称已存在,请勿重复添加"}), 401
        new_data = Tv(title=title, image=image, source=source, description=description, total_episodes=total_episodes, rating=rating, type=type,hot=hot,tags=tags)
        db.session.add(new_data)
        db.session.commit()
        return jsonify({"code": 200, "msg": "添加成功"})
 
def del_tv_by_title(title):
    """
        删除tv(根据影视名称)
    """
    with app.app_context():
        try:
            tv = Tv.query.filter_by(title=title).first()
            db.session.delete(tv)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": str(e)}), 500

        return jsonify({"code": 200, "msg": f"删除成功"})
  
def edit_tv():
    """
        修改影视
    """
    json_data = request.get_json()
    with app.app_context():
        try:

            title = json_data.get("title")
            image = json_data.get("image")
            source = json_data.get("source")
            description = json_data.get("description")
            total_episodes = json_data.get("total_episodes")
            rating = json_data.get("rating")
            type = json_data.get("type")
            hot = json_data.get("hot")
            tags = json_data.get("tags")
            id = json_data.get('id')

            if title:
                tv = Tv.query.filter_by(title=title).first()
            else:
                tv = Tv.query.filter_by(id=id).first()

            tv.image = image
            tv.source = source
            tv.description = description
            tv.total_episodes = total_episodes
            tv.rating = rating
            tv.type = type
            tv.hot = hot
            tv.tags = tags
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": str(e)}), 500

        return jsonify({"code": 200, "msg": '修改成功'})
    

def list_tv():
    """
        影视列表
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    with app.app_context():
        pagination = db.session.query(Tv).paginate(page=page, per_page=per_page)
        data = [item.to_dict() for item in pagination.items]
        return jsonify({"code": 200, "result": data,"page": page,"per_page": per_page,"total": pagination.total,"pages": pagination.pages})
    
def search_tv():
    """
        影视搜索
        pattern:匹配模式，可选值:fuzzy(模糊匹配)、exact(精确匹配)
    """
    with app.app_context():
        keyword = request.args.get('keyword')
        pattern = request.args.get('pattern', 'fuzzy', type=str).lower()  # 默认是模糊匹配
        if not keyword:  
            return jsonify({"code": 400, "msg": "关键词不能为空"}), 400  
  
        if pattern == 'exact':  
            # 精确匹配  
            tv = Tv.query.filter(Tv.title == keyword).all()  
        else:  
            # 模糊匹配  
            tv = Tv.query.filter(Tv.title.like('%' + keyword + '%')).all()  
  
        data = [item.to_dict() for item in tv]  
        return jsonify({"code": 200, "result": data})  
    
def sync_tv():
    """
        同步影视
    """
    with app.app_context():
        try:
            db.session.execute("TRUNCATE TABLE tv")
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": str(e)}), 500