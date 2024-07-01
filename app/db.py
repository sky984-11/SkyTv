"""
@ Date: 2024-04-26 16:54:11
@ LastEditors: sky
@ LastEditTime: 2024-05-11 17:15:53
@ FilePath: /SkyTunnel/app/db.py
@ Desc: 
"""


from run import app
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy


# 加载数据库
db = SQLAlchemy(app)

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
        image:影视图片(可能失效)
        source:影视来源列表，多个用\隔开(可能会经常变动)
        description:影视描述(可选)
        total_episodes:总集数(可能会经常变动)
        rating:评分(可能会经常变动)
        type:影视类型,tv_show 0/movie 1/anime 2
        tags:标签,多个用/隔开
        hot:是否热门影视(可能会经常变动)
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
    tags = db.Column(db.Text, nullable=False)
    hot = db.Column(db.Boolean, default=False)
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
            "tags":self.tags,
            "hot":self.hot,

        }

class Episodes(db.Model):
    """
        集数表
        episode:集数(可能会经常变动)
        source:播放来源(可以让用户进行播放源切换)(可能会经常变动)
        link:播放链接(可能会经常变动)
        tv_title:影视名称
    """

    __tablename__ = 'episodes'
    __table_args__ = {'extend_existing': True}

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


with app.app_context():
    db.create_all()
# 删除表
# db.drop_all()
