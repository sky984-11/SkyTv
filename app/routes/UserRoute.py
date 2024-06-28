from flask import request, jsonify,send_file
from db import User,db
from run import app
from public.user.auth import *

from config import  ProductionConfig

import random
import os
import datetime



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
        return jsonify({"code": 400, "msg": "用户名和密码不能为空"}), 400

    with app.app_context():
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"code": 401, "msg": "用户名已存在,请勿重复注册"}), 401
        new_user = User(username=username, role="user", utime=datetime.datetime.now(),avatar=avatar)
        new_user.hash_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"code": 200, "msg": "注册成功"})

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
        return jsonify({"code": 400, "msg": "用户名和密码不能为空"}), 400

    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"code": 401, "msg": "未找到该用户"}), 401
        if user.verify_password(password):
            encoded_jwt = generate_token(username, password)
            response = {
                "code": 200,
                "msg": "登录成功",
                "token": encoded_jwt,
                "user_id": user.user_id
            }
            return jsonify(response)
        else:
            return jsonify({"code": 402, "msg": "密码错误"}), 402

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
    username = request.form.get('username')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    if not username or not old_password or not new_password:
        return jsonify({"code": 400, "msg": "用户名和密码不能为空"}), 400

    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"code": 401, "msg": "未找到该用户"}), 401
        if not user.verify_password(old_password):
            return jsonify({"code": 402, "msg": "密码输入错误"}), 402
            
        user.hash_password(new_password)
        db.session.commit()
        db.session.close()
        return jsonify({'msg': '修改成功', 'code': 200})

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
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'msg': 'token未授权或过期','code':401}),401

    data = decode_token(token)
    if 'error' in data:
        return jsonify({'msg': 'token未授权或过期','code':401}),401


    with app.app_context():
        try:
            # 级联用户将删除所有用户关联的数据
            user = User.query.filter_by(user_id=user_id).first()
            if not user:
              return jsonify({"code": 401, "msg": "未找到该用户"}), 404

            if user_id != user.user_id:
              return jsonify({"code": 411, "msg": "要删除的用户不属于该授权凭证"}), 411

            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": str(e)}), 500

        return jsonify({"code": 200, "msg": f"用户注销成功"})

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
    response = {
        'code':200,'msg': 'logout success'
    }
    return jsonify(response)


def range_user_image():
    """
    发送一个随机图像
    ---
    tags:
      - user
    responses:
      200:
        description: 成功
    """

    IMAGE_URL = '/static/user/images'
    fileList = []
    user_image_path = os.getcwd() + '/static/user/images/'
    for root, dirs, files in os.walk(user_image_path):
        for image in files:
            fileList.append(IMAGE_URL + '/' + image)
    return jsonify({'msg': random.choice(fileList),'code':200})

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
    token = request.headers.get('Authorization')


    if not token:
        return jsonify({'msg': 'token未授权或过期','code':401}),401

    data = decode_token(token)
    if 'error' in data:
        return jsonify({'msg': 'token未授权或过期','code':401}),401

    with app.app_context():
        user = User.query.filter_by(username=data.get('username')).first()
        if not user:
            return jsonify({"code": 404, "msg": "用户名不存在"}), 404
        data = {
            "user_id": user.user_id,
            "username": user.username,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "qq": user.qq,
            "role": user.role,
            "ctime": user.ctime.strftime("%Y年%m月%d日 %H:%M:%S"),
            "utime": user.utime.strftime("%Y年%m月%d日 %H:%M:%S"),
        }
        response = {
        'msg': data,
        'code':200
        }
        return jsonify(data)


def upload_image():
    """上传用户头像"""
    imgBase64 = request.files.get('file')
    # 图片的md5格式
    md5 = request.form.get('md5')
    name = md5 + '.' + imgBase64.filename.split('.')[1]
    imgBase64.save(fr'./static/user/upload/{name}')

    IMAGE_URL = 'http://' + ProductionConfig.IMAGE_SERVER + \
            f'/static/user/upload/{name}'
    response = {
        'msg': {'url': IMAGE_URL},
        'code':200
    }
    return jsonify(response)

