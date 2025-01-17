'''
Description: 
Author: liupeng
Date: 2025-01-16 17:47:07
LastEditTime: 2025-01-17 10:16:56
LastEditors: liupeng
'''



from flask_cors import CORS
from flask import Blueprint

from routes.UserRoute import *
from routes.TokenRoute import *

from config import BaseConfig


# 创建蓝图
b1 = Blueprint('b1', __name__)
# 解决跨域问题
CORS(b1)

##################################### Token start #####################################
#  生成授权凭证
b1.route(f'/api/{BaseConfig.API_VERSION}/token', methods=['POST'])(get_token)
##################################### Token start #####################################


##################################### User start #####################################
# 新用户注册
b1.route(f'/api/{BaseConfig.API_VERSION}/user/register', methods=['POST'])(register)
# 用户登录
b1.route(f'/api/{BaseConfig.API_VERSION}/user/login', methods=['POST'])(login)
# 用户密码修改
b1.route(f'/api/{BaseConfig.API_VERSION}/user/password/change', methods=['POST'])(change_password)
# 用户注销
b1.route(f'/api/{BaseConfig.API_VERSION}/user/del/<int:user_id>', methods=['DELETE'])(delete_user)
# 用户随机头像
b1.route(f'/api/{BaseConfig.API_VERSION}/user/image/random', methods=['GET'])(range_user_image)
# 查询某个用户信息
b1.route(f'/api/{BaseConfig.API_VERSION}/user/info', methods=['POST'])(select_user_info)

# 用户头像上传
# b1.route(f'/api/{DefaultConfig.API_VERSION}/user/image/upload', methods=['POST'])(upload_image)
#####################################  User end  #####################################



