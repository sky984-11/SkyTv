from flask import request, jsonify, abort
from db import Video, VodDetail, db
from utils.tools import with_app_context, paginate

@with_app_context
def create_video():
    """创建一个新的Video。
    
    参数:
    - vod_title (str): 视频标题。
    - vod_type (str): 视频类型。
    - vod_score (float, optional): 视频评分。
    - vod_pic_url (str): 视频图片URL。
    - vod_pic_path (str, optional): 视频图片路径。
    
    返回:
    - dict: 新创建Video的详情。
    - int: HTTP状态码，201表示成功创建。
    
    异常:
    - 400: 输入数据缺失或无效。
    """
    data = request.json
    if 'vod_title' not in data or 'vod_type' not in data or 'vod_pic_url' not in data:
        abort(400, "缺少必要的参数'vod_title', 'vod_type', 或 'vod_pic_url'")
    if not data['vod_title'] or not data['vod_type'] or not data['vod_pic_url']:
        abort(400, "参数'vod_title', 'vod_type', 或 'vod_pic_url'无效")
    new_video = Video(vod_title=data['vod_title'], vod_type=data['vod_type'], 
                      vod_score=data.get('vod_score'), vod_pic_url=data['vod_pic_url'], 
                      vod_pic_path=data.get('vod_pic_path'))
    try:
        db.session.add(new_video)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"数据库操作失败: {e}")
    return jsonify(new_video.to_dict()), 201

@with_app_context
def get_all_videos():
    """获取所有Video的分页列表。
    
    参数:
    - page (int): 请求的页码。
    
    返回:
    - list: Video列表。
    - int: HTTP状态码，200表示成功。
    
    异常:
    - 404: 请求的页码超出范围。
    """
    page = request.args.get('page', 1, type=int)
    videos, pages = paginate(Video.query, page)
    return jsonify([video.to_dict() for video in videos]), 200

@with_app_context
def get_video(video_id):
    """根据ID获取单个Video。
    
    参数:
    - video_id (int): Video的ID。
    
    返回:
    - dict: Video的详情。
    - int: HTTP状态码，200表示成功。
    
    异常:
    - 404: Video不存在。
    """
    video = Video.query.get_or_404(video_id)
    return jsonify(video.to_dict()), 200

@with_app_context
def update_video(video_id):
    """更新一个Video。
    
    参数:
    - video_id (int): Video的ID。
    
    返回:
    - dict: 更新后的Video详情。
    - int: HTTP状态码，200表示成功。
    
    异常:
    - 404: Video不存在。
    - 400: 更新数据缺失或无效。
    """
    video = Video.query.get_or_404(video_id)
    data = request.json
    for key, value in data.items():
        if not hasattr(video, key):
            abort(400, f"无效的更新参数'{key}'")
        setattr(video, key, value)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"数据库操作失败: {e}")
    return jsonify(video.to_dict()), 200

@with_app_context
def delete_video(video_id):
    """删除一个Video。
    
    参数:
    - video_id (int): Video的ID。
    
    返回:
    - dict: 消息提示。
    - int: HTTP状态码，204表示成功删除。
    
    异常:
    - 404: Video不存在。
    """
    video = Video.query.get_or_404(video_id)
    try:
        db.session.delete(video)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"数据库操作失败: {e}")
    return jsonify({"message": "Video deleted"}), 204

@with_app_context
def add_video_and_vod_detail(data):
    """添加一个Video及其对应的VodDetail。
    
    参数:
    - data (dict): 包含视频和视频详情信息的字典。

    返回:
    - dict: 消息提示。
    - int: HTTP状态码，201表示成功创建。

    异常:
    - 400: 数据不完整或格式错误。
    - 500: 数据库操作失败。
    """
    required_fields = ['vod_title', 'vod_type', 'vod_score', 'vod_pic_url', 
                       'vod_content', 'vod_tag', 'vod_source', 'vod_episodes']
    if not all(field in data for field in required_fields):
        abort(400, "Missing required fields")

    video_data = {
        'vod_title': data['vod_title'],
        'vod_type': data['vod_type'],
        'vod_score': data['vod_score'],
        'vod_pic_url': data['vod_pic_url'],
        'vod_pic_path': data.get('vod_pic_path')  # 可能是可选字段
    }

    vod_detail_data = {
        'vod_content': data['vod_content'],
        'vod_tag': data['vod_tag'],
        'vod_source': data['vod_source'],
        'vod_episodes': data['vod_episodes'],
        'vod_episodes_index': data.get('vod_episodes_index')  # 可能是可选字段
    }

    try:
        video = Video(**video_data)
        db.session.add(video)
        db.session.flush()  # Flush to get the video's ID before adding VodDetail

        vod_detail_data['video_id'] = video.id
        vod_detail = VodDetail(**vod_detail_data)
        db.session.add(vod_detail)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"数据库操作失败: {e}")

    return jsonify({"message": "Video and VodDetail added successfully"}), 201