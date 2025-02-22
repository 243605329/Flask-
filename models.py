"""
定义模型类
"""
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

from app import db


class User(db.Model,UserMixin):
    """
    用户模型类
    """
    id = db.Column(db.Integer,primary_key=True) #id 主键
    name = db.Column(db.String(20)) #用户名
    username = db.Column(db.String(20)) #昵称
    password = db.Column(db.String(128)) #密码散列值
    is_admin = db.Column(db.Boolean, default=False)  # 新增管理员标识字段

    def set_password(self,password): 
        """
        设置密码
        """
        self.password = generate_password_hash(password)

    
    def validate_password(self,password): 
        """
        验证密码
        """
        return check_password_hash(pwhash=self.password, password=password)

class Movie(db.Model):
    """
    电影模型类
    """
    id = db.Column(db.Integer,primary_key=True) #id 主键
    title = db.Column(db.String(60)) #电影名
    year = db.Column(db.String(4)) #年份

