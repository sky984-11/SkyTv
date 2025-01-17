from flask import request
from db import User,db
from utils.auth import generate_token, decode_token
from config import  BaseConfig
from utils.tools import with_app_context,make_response
import random
import os
import datetime


def validate_token():
    token = request.headers.get("Authorization")
    if not token:
        return make_response(401, "token未授权或过期")
    data = decode_token(token)
    if "error" in data:
        return make_response(401, "token未授权或过期")
    return data

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def register_user(username, password, avatar):
    new_user = User(username=username, role="user", utime=datetime.datetime.now(), avatar=avatar)
    new_user.hash_password(password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

@with_app_context
def register():
    """
    用户注册
    ---
    tags:
      - user
    parameters:
      - in: formData
        name: username
        required: true
        description: 用户名
        type: string
      - in: formData
        name: password
        required: true
        description: 密码
        type: string
      - in: formData
        name: avatar
        description: 头像
        type: string
    responses:
      200:
        description: 成功
      400:
        description: 用户名和密码不能为空
      401:
        description: 用户名已存在
    """
    username = request.form.get("username")
    password = request.form.get("password")
    avatar = request.form.get("avatar")

    if not username or not password:
        return make_response(400, "用户名和密码不能为空")
    if get_user_by_username(username):
        return make_response(401, "用户名已存在,请勿重复注册")

    register_user(username, password, avatar)
    return make_response(200, "注册成功")

@with_app_context
def login():
    """
    用户登陆
    ---
    tags:
      - user
    parameters:
      - in: formData
        name: username
        required: true
        description: 用户名
        type: string
      - in: formData
        name: password
        required: true
        description: 密码
        type: string
      - in: formData
        name: avatar
        description: 头像
        type: string
    responses:
      200:
        description: 成功
      400:
        description: 用户名和密码不能为空
      401:
        description: 未找到该用户
      402:
        description: 密码错误
    """
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return make_response(400, "用户名和密码不能为空")

    user = get_user_by_username(username)
    if not user:
        return make_response(401, "未找到该用户")
    if user.verify_password(password):
        token = generate_token(username, password)
        return make_response(200, "登录成功", {"token": token, "user_id": user.user_id})
    return make_response(402, "密码错误")

@with_app_context
def change_password():
    """
    修改用户密码
    ---
    tags:
      - user
    parameters:
      - in: formData
        name: username
        required: true
        description: 用户名
        type: string
      - in: formData
        name: old_password
        required: true
        description: 原密码
        type: string
      - in: formData
        name: new_password
        description: 新密码
        type: string
        required: true
    responses:
      200:
        description: 成功
      400:
        description: 用户名和密码不能为空
      401:
        description: 未找到该用户
      402:
        description: 密码错误
    """
    username = request.form.get("username")
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")

    if not username or not old_password or not new_password:
        return make_response(400, "用户名和密码不能为空")

    user = get_user_by_username(username)
    if not user:
        return make_response(401, "未找到该用户")
    if not user.verify_password(old_password):
        return make_response(402, "密码错误")

    user.hash_password(new_password)
    db.session.commit()
    return make_response(200, "修改成功")

@with_app_context
def delete_user(user_id):
    """
    用户注销
    ---
    tags:
      - user
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: 要删除的用户ID
      - in: header
        name: Authorization
        type: string
        required: true
        description: 授权凭证
    responses:
      200:
        description: 成功
      401:
        description: token未授权或过期
      404:
        description: 未找到该用户
      411:
        description: 要删除的数据不属于该授权凭证
      500:
        description: 服务端错误
    """
    data = validate_token()
    if isinstance(data, tuple):
        return data  # 返回错误响应

    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return make_response(404, "未找到该用户")
    if user_id != data["user_id"]:
        return make_response(411, "要删除的用户不属于该授权凭证")

    try:
        db.session.delete(user)
        db.session.commit()
        return make_response(200, "用户注销成功")
    except Exception as e:
        db.session.rollback()
        return make_response(500, f"服务端错误: {str(e)}")

def logout():
    """
    用户退出提醒
    ---
    tags:
      - user
    responses:
      200:
        description: 成功
    """
    return make_response(200, "退出成功")


def range_user_image():
    """
    获取用户随机图像
    ---
    tags:
      - user
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: 授权凭证
    responses:
      200:
        description: 成功
    """
    data = validate_token()
    if isinstance(data, tuple):
        return data  # 返回错误响应
    image_dir = os.path.join(os.getcwd(), "static/user/images/")
    images = [f"{BaseConfig.SERVER_NAME}/static/user/images/{img}" for img in os.listdir(image_dir)]
    if not images:
        return make_response(404, "没有可用的图像")
    return make_response(200, "成功", random.choice(images))

@with_app_context
def select_user_info():
    """
    用户信息查询
    ---
    tags:
      - user
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: 授权凭证
    responses:
      200:
        description: 成功
      401:
        description: token未授权或过期
      404:
        description: 用户名不存在
    """
    data = validate_token()
    if isinstance(data, tuple):
        return data

    user = get_user_by_username(data.get("username"))
    if not user:
        return make_response(404, "用户名不存在")

    user_info = {
        "user_id": user.user_id,
        "username": user.username,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "qq": user.qq,
        "role": user.role,
        "ctime": user.ctime.strftime("%Y-%m-%d %H:%M:%S"),
        "utime": user.utime.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return make_response(200, "成功", user_info)

def upload_image():
    """上传用户头像"""
    img_file = request.files.get("file")
    md5 = request.form.get("md5")
    if not img_file or not md5:
        return make_response(400, "缺少文件或MD5值")

    ext = os.path.splitext(img_file.filename)[1]
    filename = f"{md5}{ext}"
    save_path = os.path.join("./static/user/upload/", filename)
    img_file.save(save_path)

    image_url = f"http://{BaseConfig.IMAGE_SERVER}/static/user/upload/{filename}"
    return make_response(200, "成功", {"url": image_url})

