from utils.auth import *
from flask import request
from db import User

from utils.tools import with_app_context,make_response

@with_app_context
def get_token():
    """
    生成授权凭证
    ---
    tags:
      - token
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            username:
              type: string
              description: 用户名
              required: true
            password:
              type: string
              description: 用户密码
              required: true
            exp:
              type: number
              default: 3600
              description: 过期时间
    responses:
      200:
        description: 成功
      400:
        description: 用户名和密码不能为空
      404:
        description: 用户不存在
      405:
        description: 密码错误
    """
    json_data = request.get_json()
    username = json_data.get('username')
    password = json_data.get('password')
    exp = json_data.get('exp')
    
    if not username or not password:
        return make_response(400, "用户名和密码不能为空")

    user = User.query.filter_by(username=username).first()
    if not user:
      return make_response(404, "用户不存在")
    if not user.verify_password(password):
      return make_response(405, "密码错误")

    encoded_jwt = generate_token(username, password, exp) if exp else generate_token(username, password)
    return make_response(200, "成功",{'token':encoded_jwt})