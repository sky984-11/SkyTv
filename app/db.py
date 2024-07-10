'''
Description: 
Author: sky
Date: 2024-07-06 08:11:16
LastEditTime: 2024-07-10 13:58:48
LastEditors: sky
'''

from run import app
from sqlalchemy.orm import relationship,declarative_base
from sqlalchemy import UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect

from datetime import datetime

# 加载数据库
db = SQLAlchemy(app)

Base = declarative_base()

class BaseModel(db.Model):
    """
    抽象基类，为所有子类添加创建时间和更新时间字段。
    """
    __abstract__ = True

    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def to_dict(self):
        """使用反射动态生成字典，减少维护成本"""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Source(BaseModel):
    __tablename__ = 'source'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, comment='源名称')
    url = db.Column(db.String(255), nullable=False, comment='源URL')
    main = db.Column(db.Boolean, default=False, comment='是否为主要源')
    disable = db.Column(db.Boolean, default=False, comment='是否禁用')

class Video(BaseModel):
    __tablename__ = 'video'
    __table_args__ = (
        UniqueConstraint('vod_title', 'vod_type', name='uq_vod_title_vod_type'),
        {'extend_existing': True}
    )
    id = db.Column(db.Integer, primary_key=True)
    vod_title = db.Column(db.String(255), nullable=False, comment='视频标题')
    vod_type = db.Column(db.String(50), nullable=False, comment='视频类型')
    vod_score = db.Column(db.Float, comment='视频评分')
    vod_pic_url = db.Column(db.Text, nullable=False, comment='视频图片URL')
    vod_pic_path = db.Column(db.String(255), comment='视频图片路径')
    vod_detail = relationship('VodDetail', backref='video_backref', cascade='all,delete-orphan', lazy='joined')
    
class VodDetail(BaseModel):
    __tablename__ = 'vod_detail'
    __table_args__ = (
        UniqueConstraint('video_id', 'vod_episodes', name='uq_vod_detail_unique'),
        {'extend_existing': True}
    )
    id = db.Column(db.Integer, primary_key=True)
    vod_content = db.Column(db.Text, nullable=False, comment='视频详情内容')
    vod_tag = db.Column(db.Text, nullable=False, comment='视频标签')
    vod_episodes = db.Column(db.String(255), comment='视频集数')
    vod_episodes_index = db.Column(db.Integer, comment='视频集数索引')
    play_url = relationship('PlayUrl', backref='vod_details_backref', cascade='all,delete-orphan', lazy='joined')
    
    video_id = db.Column(db.Integer, db.ForeignKey('video.id', ondelete='CASCADE'), nullable=False)

class PlayUrl(BaseModel):
    __tablename__ = 'play_url'
    __table_args__ = (
        UniqueConstraint('vod_detail_id','play_source', name='uq_play_url_unique'),
        {'extend_existing': True}
    )
    id = db.Column(db.Integer, primary_key=True)
    play_source = db.Column(db.String(255), nullable=False, comment='播放来源')
    play_status = db.Column(db.Boolean, default=True, comment='播放状态')
    play_url = db.Column(db.Text, nullable=False, unique=True, comment='播放URL')
    
    vod_detail_id = db.Column(db.Integer, db.ForeignKey('vod_detail.id', ondelete='CASCADE'), nullable=False)

with app.app_context():
    db.create_all()
# 删除表
# db.drop_all()
