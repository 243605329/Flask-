"""
Flask 项目
"""
import os
import sys
import click
from flask import Flask,url_for,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

"""
适配 Windows 和 Linux 系统
"""
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

"""
配置数据库
"""
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db') # 数据库地址
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
db = SQLAlchemy(app) # 初始化数据库






from models import User,Movie
@app.cli.command()
@click.option('--drop',is_flag=True,help='Create after drop.')
def initdb(drop):
    """
    初始化数据库
    """
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    """
    生成虚拟数据
    """
    db.create_all()
    name	=	'Study Flask'
    v_movies	=	[
    {'title':	'My	Neighbor	Totoro',	'year':	'1988'},
    {'title':	'Dead	Poets	Society',	'year':	'1989'},
    {'title':	'A	Perfect	World',	'year':	'1993'},
    {'title':	'Leon',	'year':	'1994'},
    {'title':	'Mahjong',	'year':	'1996'},
    {'title':	'Swallowtail	Butterfly',	'year':	'1996'},
    {'title':	'King	of	Comedy',	'year':	'1999'},
    {'title':	'Devils	on	the	Doorstep',	'year':	'1999'},
    {'title':	'WALL-E',	'year':	'2008'},
    {'title':	'The	Pork	of	Music',	'year':	'2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in v_movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html',movies=movies)






