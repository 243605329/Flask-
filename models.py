"""
定义模型类
"""

from app import db
import click

class User(db.Model):
    """
    用户模型类
    """
    id = db.Column(db.Integer,primary_key=True) #id 主键
    name = db.Column(db.String(20)) #用户名

class Movie(db.Model):
    """
    电影模型类
    """
    id = db.Column(db.Integer,primary_key=True) #id 主键
    title = db.Column(db.String(60)) #电影名
    year = db.Column(db.String(4)) #年份

