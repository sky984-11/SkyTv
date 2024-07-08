'''
Description: 路由
Author: sky
Date: 2024-07-06 14:12:59
LastEditTime: 2024-07-08 14:23:20
LastEditors: sky
'''


from flask_cors import CORS
from flask import Blueprint
from config import DefaultConfig

from routes.SourceRoute import create_source,get_all_sources,get_source,update_source,delete_source,get_main_sources
from routes.VideoRoute import create_video,get_all_videos,get_video,update_video,delete_video,add_video_and_vod_detail,get_video_by_title_and_type
from routes.VodDetailRoute import create_vod_detail,get_all_vod_details,get_vod_detail,update_vod_detail,delete_vod_detail,get_vod_detail_id
from routes.PlayUrlRoute import create_play_url,get_all_play_urls,get_play_url,update_play_url,delete_play_url,get_play_url_by_details

# 创建蓝图
b1 = Blueprint('b1', __name__)
# 解决跨域问题
CORS(b1)


##################################### Source Start #####################################
# 添加来源
b1.route(f'/api/{DefaultConfig.API_VERSION}/source', methods=['POST'])(create_source)
# 获取所有来源
b1.route(f'/api/{DefaultConfig.API_VERSION}/source', methods=['GET'])(get_all_sources)
# 根据名称获取来源
b1.route(f'/api/{DefaultConfig.API_VERSION}/source/<string:source_name>', methods=['GET'])(get_source)
# 根据修改来源
b1.route(f'/api/{DefaultConfig.API_VERSION}/source/<int:source_id>', methods=['PUT', 'PATCH'])(update_source)
# 删除来源
b1.route(f'/api/{DefaultConfig.API_VERSION}/source/<int:source_id>', methods=['DELETE'])(delete_source)
# 查询主要来源
b1.route(f'/api/{DefaultConfig.API_VERSION}/source/main', methods=['GET'])(get_main_sources)
#####################################  Source End  #####################################

##################################### Video Start #####################################
# 添加视频
b1.route(f'/api/{DefaultConfig.API_VERSION}/video', methods=['POST'])(create_video)
# 获取所有视频
b1.route(f'/api/{DefaultConfig.API_VERSION}/video', methods=['GET'])(get_all_videos)
# 根据id获取视频
b1.route(f'/api/{DefaultConfig.API_VERSION}/video/<int:video_id>', methods=['GET'])(get_video)
# 根据标题和类型获取视频
b1.route(f'/api/{DefaultConfig.API_VERSION}/video/<string:vod_title>/<string:vod_type>', methods=['GET'])(get_video_by_title_and_type)
# 根据id修改视频
b1.route(f'/api/{DefaultConfig.API_VERSION}/video/<int:video_id>', methods=['PUT', 'PATCH'])(update_video)
# 删除视频
b1.route(f'/api/{DefaultConfig.API_VERSION}/video/<int:video_id>', methods=['DELETE'])(delete_video)
# 添加视频和视频详情
b1.route(f'/api/{DefaultConfig.API_VERSION}/video/video_and_vod_detail', methods=['POST'])(add_video_and_vod_detail)
##################################### Video End  #####################################

##################################### VodDetail Start #####################################
# 添加视频详情
b1.route(f'/api/{DefaultConfig.API_VERSION}/vod-detail', methods=['POST'])(create_vod_detail)
# 获取所有视频详情
b1.route(f'/api/{DefaultConfig.API_VERSION}/vod-detail', methods=['GET'])(get_all_vod_details)
# 根据id获取视频详情
b1.route(f'/api/{DefaultConfig.API_VERSION}/vod-detail/<int:vod_detail_id>', methods=['GET'])(get_vod_detail)
# 根据id修改视频详情
b1.route(f'/api/{DefaultConfig.API_VERSION}/vod-detail/<int:vod_detail_id>', methods=['PUT', 'PATCH'])(update_vod_detail)
# 删除视频详情
b1.route(f'/api/{DefaultConfig.API_VERSION}/vod-detail/<int:vod_detail_id>', methods=['DELETE'])(delete_vod_detail)
# 根据标题、来源、视频集数获取vod_detail_id
b1.route(f'/api/{DefaultConfig.API_VERSION}/vod-detail/<string:vod_title>/<string:vod_source>/<string:vod_episodes>', methods=['GET'])(get_vod_detail_id)
##################################### VodDetail End  #####################################

##################################### PlayUrl Start #####################################
# 添加播放url
b1.route(f'/api/{DefaultConfig.API_VERSION}/play_url', methods=['POST'])(create_play_url)
# 获取所有播放url
b1.route(f'/api/{DefaultConfig.API_VERSION}/play_url', methods=['GET'])(get_all_play_urls)
# 根据id获取播放url
b1.route(f'/api/{DefaultConfig.API_VERSION}/play_url/<int:play_url_id>', methods=['GET'])(get_play_url)
# 根据id修改播放url
b1.route(f'/api/{DefaultConfig.API_VERSION}/play_url/<int:play_url_id>', methods=['PUT', 'PATCH'])(update_play_url)
# 删除播放url
b1.route(f'/api/{DefaultConfig.API_VERSION}/play_url/<int:play_url_id>', methods=['DELETE'])(delete_play_url)
# 根据播放标题、播放来源、视频集数获取播放url
b1.route(f'/api/{DefaultConfig.API_VERSION}/play_url/<string:play_title>/<string:play_from>/<string:vod_episodes>', methods=['GET'])(get_play_url_by_details)
##################################### PlayUrl End  #####################################


