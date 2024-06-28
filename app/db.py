"""
@ Date: 2024-04-26 16:54:11
@ LastEditors: sky
@ LastEditTime: 2024-05-11 17:15:53
@ FilePath: /SkyTunnel/app/db.py
@ Desc: 
"""


from run import app
import datetime
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy

from passlib.apps import custom_app_context as pwd_context

# 加载数据库
db = SQLAlchemy(app)

class User(db.Model):
    """
        用户表
        user_id:主键，自动递增的整数。
        username:登陆账户，可以为手机号或者邮箱
        password:md5密码加密字符串
        nickname:用户昵称，可为空。
        avatar:用户头像的文件名称。可为空。
        qq:用户的QQ号码,可为空。
        role:用户角色，默认用户。(admin,user)。
        ctime:记录时间，采用 TIMESTAMP 类型，采用当前时间。
        utime:最后一次更新的时间，不可为空。
        token:授权凭证,可为空。
        oauth_secret:OAuth 客户端密钥,可为空。
        oauth_id:OAuth 客户端id,可为空。
    """
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    # nullable是否为空，unique唯一约束
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=True, unique=True)
    password = db.Column(db.String(150), nullable=True)
    nickname = db.Column(db.String(50), nullable=True)
    avatar = db.Column(db.String(50), nullable=True)
    qq = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(250), default='user')
    ctime = db.Column(db.DateTime, default=datetime.datetime.now)
    utime = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String(255), nullable=True)
    oauth_secret = db.Column(db.String(255), nullable=True)
    oauth_id = db.Column(db.String(255), nullable=True)

    # records = relationship('Tunner', backref='tunner',cascade='all,delete-orphan')

    def hash_password(self, password):  # 给密码加密方法
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):  # 验证密码方法
        return pwd_context.verify(password, self.password)
    

class Source(db.Model):
    """
        来源表
        name:网站名称,唯一值
        url:网站首页地址
        main:是否为主要地址,默认为false(只能存在一个)
        ping:网站是否可以ping通,默认为True
        disable:是否禁用当前源(无法ping通时自动禁用)
    """
    __tablename__ = 'source'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    url = db.Column(db.String(255), nullable=False)
    main = db.Column(db.Boolean, default=False)
    ping = db.Column(db.Boolean, default=True)
    disable = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "main": self.main,
            "ping":self.ping,
            "disable":self.disable,
        }

class Tv(db.Model):
    """
        影视表
        title:影视名称，唯一值
        image:影视图片
        source:影视来源列表，多个用\隔开
        description:影视描述(可选)
        total_episodes:总集数
        rating:评分
        type:影视类型,tv_show 0/movie 1/anime 2
    """
    __tablename__ = 'tv'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    image = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(255),nullable=True)
    description = db.Column(db.Text, nullable=True)
    total_episodes = db.Column(db.String(255),nullable=True)
    rating = db.Column(db.String(255),nullable=True)
    type = db.Column(db.Integer)
    episodes = relationship('Episodes', backref='episodes',cascade='all,delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "image": self.image,
            "source": self.source,
            "description":self.description,
            "total_episodes":self.total_episodes,
            "rating":self.rating,
            "type":self.type,
        }

class Episodes(db.Model):
    """
        集数表
        episode:集数
        source:播放来源(可以让用户进行播放源切换)
        link:播放链接
        tv_title:影视名称
    """
    id = db.Column(db.Integer, primary_key=True)
    episode = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(255),nullable=True)
    link = db.Column(db.Text, nullable=True)
    
    tv_title= db.Column(db.String(255), db.ForeignKey(
        'tv.title', ondelete='CASCADE'), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "episode": self.episode,
            "source": self.source,
            "link": self.link,
            "tv_title":self.tv_title,
        }
    

# class Rank(db.Model):
#     """
#         排行表
#     """


with app.app_context():
    db.create_all()
# 删除表
# db.drop_all()
