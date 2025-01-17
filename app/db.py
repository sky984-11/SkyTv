'''
Description: 
Author: liupeng
Date: 2025-01-16 17:47:07
LastEditTime: 2025-01-17 09:53:34
LastEditors: liupeng
'''


from run import app

from sqlalchemy.orm import relationship, declarative_base
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.inspection import inspect

# 加载数据库
db = SQLAlchemy(app)

Base = declarative_base()

class BaseModel(db.Model):
    """
    抽象基类，为所有子类添加创建时间和更新时间字段。
    """
    __abstract__ = True

    ctime = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    utime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def to_dict(self):
        """使用反射动态生成字典，减少维护成本"""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

class User(BaseModel):
    """
        用户表
        user_id:主键，自动递增的整数。
        username:登陆账户，可以为手机号或者邮箱
        password:密码
        nickname:用户昵称，可为空。
        avatar:用户头像的文件名称。可为空。
        qq:用户的QQ号码,可为空。
        role:用户角色，默认用户。(admin,user)。
        token:授权凭证,可为空。
        oauth_secret:OAuth 客户端密钥,可为空。
        oauth_id:OAuth 客户端id,可为空。
    """
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    # nullable是否为空，unique唯一约束
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    nickname = db.Column(db.String(50), nullable=True)
    avatar = db.Column(db.String(50), nullable=True)
    qq = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(250), default='user')
    token = db.Column(db.String(255), nullable=True)
    oauth_secret = db.Column(db.String(255), nullable=True)
    oauth_id = db.Column(db.String(255), nullable=True)

    def hash_password(self, password):  # 给密码加密方法
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):  # 验证密码方法
        return pwd_context.verify(password, self.password)



with app.app_context():
    db.create_all()
# 删除表
# db.drop_all()
