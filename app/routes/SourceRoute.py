from flask import request, jsonify, abort
from db import Source, db
from utils.tools import with_app_context,paginate

@with_app_context
def create_source():
    """创建一个新的Source。
    
    参数:
    - name (str): Source名称。
    - url (str): Source的URL。
    - main (bool, optional): 是否为主要Source，默认为False。
    - disable (bool, optional): 是否禁用Source，默认为False。
    
    返回:
    - dict: 新创建Source的详情。
    - int: HTTP状态码，201表示成功创建。
    
    异常:
    - 400: 输入数据缺失或无效。
    """
    data = request.json
    if 'name' not in data or 'url' not in data:
        abort(400, "缺少必要的参数'name'或'url'")
    if not data['name'] or not data['url']:
        abort(400, "参数'name'或'url'无效")
    new_source = Source(name=data['name'], url=data['url'], main=data.get('main', False), disable=data.get('disable', False))
    try:
        db.session.add(new_source)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"数据库操作失败: {e}")
    return jsonify(new_source.to_dict()), 201

@with_app_context
def get_all_sources():
    """获取所有Source的分页列表，可选择是否包括disable为True的记录。
    
    参数:
    - page (int): 请求的页码。
    - include_disabled (bool): 是否包括disable为True的记录，默认为False。
    
    返回:
    - list: Source列表。
    - int: HTTP状态码，200表示成功。
    
    异常:
    - 404: 请求的页码超出范围。
    """
    page = request.args.get('page', 1, type=int)
    include_disabled = request.args.get('include_disabled', 'false').lower() == 'true'
    query = Source.query
    if not include_disabled:
        query = query.filter_by(disable=False)
    sources, pages = paginate(query, page)
    return jsonify([source.to_dict() for source in sources]), 200

@with_app_context
def get_source(source_name):
    """根据name获取单个Source。
    
    参数:
    - source_name (str): Source的名称。
    
    返回:
    - dict: Source的详情。
    - int: HTTP状态码，200表示成功。
    
    异常:
    - 404: Source不存在。
    """
    source = Source.query.filter_by(name=source_name).first_or_404(description=f"Source '{source_name}' not found")
    return jsonify(source.to_dict()), 200

@with_app_context
def update_source(source_id):
    """更新一个Source。
    
    参数:
    - source_id (int): Source的ID。
    
    返回:
    - dict: 更新后的Source详情。
    - int: HTTP状态码，200表示成功。
    
    异常:
    - 404: Source不存在。
    - 400: 更新数据缺失或无效。
    """
    source = Source.query.get_or_404(source_id)
    data = request.json
    for key, value in data.items():
        if not hasattr(source, key):
            abort(400, f"无效的更新参数'{key}'")
        setattr(source, key, value)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"数据库操作失败: {e}")
    return jsonify(source.to_dict()), 200

@with_app_context
def delete_source(source_id):
    """删除一个Source。
    
    参数:
    - source_id (int): Source的ID。
    
    返回:
    - dict: 消息提示。
    - int: HTTP状态码，204表示成功删除。
    
    异常:
    - 404: Source不存在。
    """
    source = Source.query.get_or_404(source_id)
    try:
        db.session.delete(source)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"数据库操作失败: {e}")
    return jsonify({"message": "Source deleted"}), 204

@with_app_context
def get_main_sources():
    """查询所有主要且未禁用的Source。
    
    返回:
    - list of dict: 主要源的信息列表。
    
    异常:
    - 500: 数据库查询或操作失败。
    """
    try:
        main_sources = Source.query.filter_by(main=True, disable=False).all()
        return jsonify([source.to_dict() for source in main_sources]), 200
    except Exception as e:
        abort(500, f"数据库操作失败: {e}")