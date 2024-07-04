"""
@ Date: 2024-04-26 15:31:44
@ LastEditors: sky
@ LastEditTime: 2024-05-08 10:11:21
@ FilePath: /SkyTunnel/app/router.py
@ Desc: 
"""


from flask_cors import CORS
from flask import Blueprint

from routes.SourceRoute import *
from routes.TvRoute import *
from routes.EpisodesRoute import add_episodes,list_episodes



from config import DefaultConfig


# 创建蓝图
b1 = Blueprint('b1', __name__)
# 解决跨域问题
CORS(b1)


# ##################################### Source Start #####################################
# 添加来源
b1.route(f'/api/{DefaultConfig.API_VERSION}/source/add', methods=['POST'])(add_source)
# 删除来源(根据id)
b1.route(f'/api/{DefaultConfig.API_VERSION}/source/del/id/<int:id>', methods=['DELETE'])(del_source_by_id)
# 删除来源(根据名称)
b1.route(f'/api/{DefaultConfig.API_VERSION}/source/del/name/<string:name>', methods=['DELETE'])(del_source_by_name)
#  修改来源地址
b1.route(f'/api/{DefaultConfig.API_VERSION}/source/edit/url', methods=['POST'])(edit_source_url)
#  设置主要来源
b1.route(f'/api/{DefaultConfig.API_VERSION}/source/edit/main', methods=['POST'])(edit_source_main)
#  是否禁用来源
b1.route(f'/api/{DefaultConfig.API_VERSION}/source/edit/disable', methods=['POST'])(edit_source_disable)
#  是否ping通来源
b1.route(f'/api/{DefaultConfig.API_VERSION}/source/edit/ping', methods=['POST'])(edit_source_ping)
# 来源列表
b1.route(f'/api/{DefaultConfig.API_VERSION}/source/list', methods=['GET'])(list_source)
# #####################################  Source End  #####################################

# ##################################### Tv Start #####################################
# 添加影视
b1.route(f'/api/{DefaultConfig.API_VERSION}/tv/add', methods=['POST'])(add_tv)
# 删除影视(根据名称)
b1.route(f'/api/{DefaultConfig.API_VERSION}/tv/del/title/<string:title>', methods=['DELETE'])(del_tv_by_title)
#  修改影视
b1.route(f'/api/{DefaultConfig.API_VERSION}/tv/edit', methods=['POST'])(edit_tv)
# 影视列表
b1.route(f'/api/{DefaultConfig.API_VERSION}/tv/list', methods=['GET'])(list_tv)
# 影视搜索
b1.route(f'/api/{DefaultConfig.API_VERSION}/tv/search', methods=['GET'])(search_tv)
# 同步影视
b1.route(f'/api/{DefaultConfig.API_VERSION}/tv/sync', methods=['POST'])(sync_tv)
#删除所有影视
b1.route(f'/api/{DefaultConfig.API_VERSION}/tv/del/all', methods=['DELETE'])(del_all_tv)
# 热门影视
b1.route(f'/api/{DefaultConfig.API_VERSION}/tv/list/hot', methods=['GET'])(list_hot_tv)
# 关闭所有热门影视
b1.route(f'/api/{DefaultConfig.API_VERSION}/tv/close/hot', methods=['GET'])(close_all_hot_tv)
# #####################################  Tv End  #####################################

# ##################################### Episodes Start #####################################
# 添加影视集数
b1.route(f'/api/{DefaultConfig.API_VERSION}/episodes/add', methods=['POST'])(add_episodes)
# 查看某个影视的所有集数
b1.route(f'/api/{DefaultConfig.API_VERSION}/episodes/list', methods=['POST'])(list_episodes)
# #####################################  Episodes End  #####################################

# ##################################### User start #####################################
# # 新用户注册
# b1.route(f'/api/{DefaultConfig.API_VERSION}/user/register', methods=['POST'])(register)
# # 用户登录
# b1.route(f'/api/{DefaultConfig.API_VERSION}/user/login', methods=['POST'])(login)
# # 用户密码修改
# b1.route(f'/api/{DefaultConfig.API_VERSION}/user/password/change', methods=['POST'])(change_password)
# # 用户注销
# b1.route(f'/api/{DefaultConfig.API_VERSION}/user/del/<int:user_id>', methods=['DELETE'])(delete_user)
# # 用户退出
# b1.route(f'/api/{DefaultConfig.API_VERSION}/user/logout', methods=['GET'])(logout)
# # 用户随机头像
# b1.route(f'/api/{DefaultConfig.API_VERSION}/user/image/random', methods=['GET'])(range_user_image)
# # 查询某个用户信息
# b1.route(f'/api/{DefaultConfig.API_VERSION}/user/info', methods=['POST'])(select_user_info)

# # 用户头像上传
# # b1.route(f'/api/{DefaultConfig.API_VERSION}/user/image/upload', methods=['POST'])(upload_image)
# #####################################  User end  #####################################

# ##################################### lucky start #####################################

# # lucky webhook数据同步
# b1.route(f'/api/{DefaultConfig.API_VERSION}/lucky/webhook/sync', methods=['POST'])(sync_webhook)

# # lucky stunrule列表
# b1.route(f'/api/{DefaultConfig.API_VERSION}/lucky/stunrule/list', methods=['GET'])(stunrule_list)

# # lucky 规则删除
# b1.route(f'/api/{DefaultConfig.API_VERSION}/lucky/del/<int:stun_id>', methods=['DELETE'])(delete_stunrule)

# # lucky 规则修改
# b1.route(f'/api/{DefaultConfig.API_VERSION}/lucky/edit', methods=['POST'])(edit_stunrule)
# #####################################  lucky end  #####################################



