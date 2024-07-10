from flask import request, jsonify, abort
from db import PlayUrl, db,VodDetail
from utils.tools import with_app_context, paginate
from sqlalchemy.orm import joinedload



@with_app_context
def create_play_url():
    """创建一个新的PlayUrl。
    
    参数:
    - play_from (str): 播放来源。
    - play_status (bool): 播放状态。
    - play_url (str): 播放URL。
    - vod_detail_id (int): 关联的VodDetail ID。
    
    返回:
    - dict: 新创建PlayUrl的详情。
    - int: HTTP状态码，201表示成功创建。
    
    异常:
    - 400: 输入数据缺失或无效。
    """
    data = request.json
    required_fields = ['play_from', 'play_url', 'vod_detail_id']
    if not all(field in data for field in required_fields):
        abort(400, "缺少必要的参数")
    new_play_url = PlayUrl(
        play_from=data['play_from'],
        play_status=data.get('play_status', True),
        play_url=data['play_url'],
        vod_detail_id=data['vod_detail_id']
    )
    try:
        db.session.add(new_play_url)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"数据库操作失败: {e}")
    return jsonify(new_play_url.to_dict()), 201


@with_app_context
def get_all_play_urls():
    """获取所有PlayUrl的分页列表。
    
    参数:
    - page (int): 请求的页码。
    
    返回:
    - list: PlayUrl列表。
    - int: HTTP状态码，200表示成功。
    
    异常:
    - 404: 请求的页码超出范围。
    """
    page = request.args.get('page', 1, type=int)
    play_urls, pages = paginate(PlayUrl.query, page)
    return jsonify([pu.to_dict() for pu in play_urls]), 200


@with_app_context
def get_play_url(play_url_id):
    """根据ID获取单个PlayUrl。
    
    参数:
    - play_url_id (int): PlayUrl的ID。
    
    返回:
    - dict: PlayUrl的详情。
    - int: HTTP状态码，200表示成功。
    
    异常:
    - 404: PlayUrl不存在。
    """
    play_url = PlayUrl.query.get_or_404(play_url_id)
    return jsonify(play_url.to_dict()), 200


@with_app_context
def update_play_url(play_url_id):
    """更新一个PlayUrl。
    
    参数:
    - play_url_id (int): PlayUrl的ID。
    
    返回:
    - dict: 更新后的PlayUrl详情。
    - int: HTTP状态码，200表示成功。
    
    异常:
    - 404: PlayUrl不存在。
    - 400: 更新数据缺失或无效。
    """
    play_url = PlayUrl.query.get_or_404(play_url_id)
    data = request.json
    for key, value in data.items():
        if not hasattr(play_url, key):
            abort(400, f"无效的更新参数'{key}'")
        setattr(play_url, key, value)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"数据库操作失败: {e}")
    return jsonify(play_url.to_dict()), 200


@with_app_context
def delete_play_url(play_url_id):
    """删除一个PlayUrl。
    
    参数:
    - play_url_id (int): PlayUrl的ID。
    
    返回:
    - dict: 消息提示。
    - int: HTTP状态码，204表示成功删除。
    
    异常:
    - 404: PlayUrl不存在。
    """
    play_url = PlayUrl.query.get_or_404(play_url_id)
    try:
        db.session.delete(play_url)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"数据库操作失败: {e}")
    return jsonify({"message": "PlayUrl deleted"}), 204