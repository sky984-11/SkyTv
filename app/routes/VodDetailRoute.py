from flask import request, jsonify, abort
from db import VodDetail, db,Video
from utils.tools import with_app_context, paginate

@with_app_context
def create_vod_detail():
    """创建一个新的VodDetail。
    
    参数:
    - vod_content (str): 视频详情内容。
    - vod_tag (str): 视频标签。
    - vod_source (str): 视频来源。
    - vod_episodes (str): 视频集数。
    - vod_total_episodes (str): 视频总集数。
    - vod_episodes_index (int): 视频集数索引。
    - video_id (int): 关联的Video ID。
    
    返回:
    - dict: 新创建VodDetail的详情。
    - int: HTTP状态码，201表示成功创建。
    
    异常:
    - 400: 输入数据缺失或无效。
    """
    data = request.json
    required_fields = ['vod_content', 'vod_tag', 'video_id']
    if not all(field in data for field in required_fields):
        abort(400, "缺少必要的参数")
    new_vod_detail = VodDetail(
        vod_content=data['vod_content'],
        vod_tag=data['vod_tag'],
        vod_source=data.get('vod_source'),
        vod_episodes=data.get('vod_episodes'),
        vod_total_episodes=data.get('vod_total_episodes'),
        vod_episodes_index=data.get('vod_episodes_index'),
        video_id=data['video_id']
    )
    try:
        db.session.add(new_vod_detail)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"数据库操作失败: {e}")
    return jsonify(new_vod_detail.to_dict()), 201

@with_app_context
def get_all_vod_details():
    """获取所有VodDetail的分页列表。
    
    参数:
    - page (int): 请求的页码。
    
    返回:
    - list: VodDetail列表。
    - int: HTTP状态码，200表示成功。
    
    异常:
    - 404: 请求的页码超出范围。
    """
    page = request.args.get('page', 1, type=int)
    vod_details, pages = paginate(VodDetail.query, page)
    return jsonify([vd.to_dict() for vd in vod_details]), 200

@with_app_context
def get_vod_detail(vod_detail_id):
    """根据ID获取单个VodDetail。
    
    参数:
    - vod_detail_id (int): VodDetail的ID。
    
    返回:
    - dict: VodDetail的详情。
    - int: HTTP状态码，200表示成功。
    
    异常:
    - 404: VodDetail不存在。
    """
    vod_detail = VodDetail.query.get_or_404(vod_detail_id)
    return jsonify(vod_detail.to_dict()), 200

@with_app_context
def update_vod_detail(vod_detail_id):
    """更新一个VodDetail。
    
    参数:
    - vod_detail_id (int): VodDetail的ID。
    
    返回:
    - dict: 更新后的VodDetail详情。
    - int: HTTP状态码，200表示成功。
    
    异常:
    - 404: VodDetail不存在。
    - 400: 更新数据缺失或无效。
    """
    vod_detail = VodDetail.query.get_or_404(vod_detail_id)
    data = request.json
    for key, value in data.items():
        if not hasattr(vod_detail, key):
            abort(400, f"无效的更新参数'{key}'")
        setattr(vod_detail, key, value)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"数据库操作失败: {e}")
    return jsonify(vod_detail.to_dict()), 200

@with_app_context
def delete_vod_detail(vod_detail_id):
    """删除一个VodDetail。
    
    参数:
    - vod_detail_id (int): VodDetail的ID。
    
    返回:
    - dict: 消息提示。
    - int: HTTP状态码，204表示成功删除。
    
    异常:
    - 404: VodDetail不存在。
    """
    vod_detail = VodDetail.query.get_or_404(vod_detail_id)
    try:
        db.session.delete(vod_detail)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"数据库操作失败: {e}")
    return jsonify({"message": "VodDetail deleted"}), 204