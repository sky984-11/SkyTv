from flask import request, jsonify, abort
from db import Video, VodDetail, PlayUrl, db,Source
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
    - vod_total_episodes (str): 视频总集数。
    
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
    per_page = request.args.get('per_page', 20, type=int)
    active_type = request.args.get('active_type', '电视剧')
    query = db.session.query(Video).filter_by(vod_type=active_type)
    pagination = query.paginate(page=page, per_page=per_page)
    data = [item.to_dict() for item in pagination.items]
    return  jsonify({"code": 200, "result": data,"page": page,"per_page": per_page,"total": pagination.total,"pages": pagination.pages}), 200

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
def sync_video():
    """同步视频信息及其详细内容和播放链接至数据库。
    
    参数:
    - data (dict): 从请求中获取的包含视频信息、详情及播放链接的字典。

    返回:
    - dict: 成功消息提示。
    - int: HTTP状态码，201表示成功创建。

    异常:
    - 400: 缺少必要的数据字段。
    - 500: 数据库操作失败。
    """
    data = request.json

    required_fields = ['vod_title', 'vod_type', 'vod_pic_url', 
                       'vod_content', 'vod_tag', 'play_from', 'vod_episodes', 'play_url','vod_total_episodes']
    if not all(field in data for field in required_fields):
        abort(400, "缺少必要的数据字段")

    try:
        video = Video.query.filter_by(vod_title=data['vod_title'], vod_type=data['vod_type'],vod_total_episodes=data['vod_total_episodes']).first()
        if not video:
            video = Video(
                vod_title=data['vod_title'],
                vod_type=data['vod_type'],
                vod_pic_url=data['vod_pic_url'],
                vod_total_episodes = data['vod_total_episodes']
            )
            db.session.add(video)
            db.session.flush() 
        else:
            source = Source.query.filter_by(main=True).first()
            print('查询主要源')
            if not source:
                abort(400, "缺少主要源")
            if source.name == data['play_from']:   # 只更新主要源
                video.vod_pic_url = data['vod_pic_url']
                video.vod_total_episodes = data['vod_total_episodes']


        # 获取或创建VodDetail
        vod_detail = VodDetail.query.filter_by(video_id=video.id, vod_episodes=data['vod_episodes']).first()
        if not vod_detail:
            print('没获取到开始添加')
            vod_detail = VodDetail(
                vod_content=data['vod_content'],
                vod_tag=data['vod_tag'],
                vod_episodes=data['vod_episodes'],
                vod_episodes_index=data.get('vod_episodes_index'),
                video_id=video.id
            )
            db.session.add(vod_detail)

        # 获取或创建PlayUrl
        play_url = PlayUrl.query.filter_by(vod_detail_id=vod_detail.id, play_from=data['play_from']).first()
        if not play_url:
            play_url = PlayUrl(
                play_from=data['play_from'],
                play_status=data['play_status'],
                play_url=data['play_url'],
                vod_detail_id=vod_detail.id
            )
            db.session.add(play_url)
        else:
            play_url.play_status = data['play_status']
            play_url.play_url = data['play_url']
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"数据库操作失败: {e}")
    return jsonify({'message': '视频信息同步成功'}), 201

@with_app_context
def list_hot_video():
    """
    根据video_list中的标题从数据库中查找并返回视频数据。
    """
    # 假设video_list是一个包含视频标题的列表
    video_titles = ['咒术回战']  # 示例，替换为实际的video_list
    
    # 创建一个空列表来存储找到的视频
    found_videos = []
    
    # 遍历每个标题，从数据库中查找对应的视频
    for title in video_titles:
        query = db.session.query(Video).filter_by(vod_title=title).first()
        if query is not None:
            found_videos.append(query)
    
    # 将查询结果转换为字典列表
    data = [video.to_dict() for video in found_videos]
    
    # 返回JSON响应
    return jsonify({"code": 200, "result": data})
    
@with_app_context
def search_video():
    """
        视频搜索
        pattern:匹配模式，可选值:fuzzy(模糊匹配)、exact(精确匹配)
    """
    keyword = request.args.get('keyword')
    pattern = request.args.get('pattern', 'fuzzy', type=str).lower()  # 默认是模糊匹配
    if not keyword:  
        return jsonify({"code": 400, "msg": "关键词不能为空"}), 400  
  
    if pattern == 'exact':  
        # 精确匹配  
        video = Video.query.filter(Video.vod_title == keyword).all()  
    else:  
        # 模糊匹配  
        video = Video.query.filter(Video.vod_title.like('%' + keyword + '%')).all()  
  
    data = [item.to_dict() for item in video]  
    return jsonify({"code": 200, "result": data})  