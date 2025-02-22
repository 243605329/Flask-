"""
Flask 项目
"""
import os
import sys
import click
from flask import Flask,url_for,render_template,request,flash,redirect,session
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
app.config['SECRET_KEY'] = 'dev' # 等同于 app.secret_key = 'dev'
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
    v_movies =[
        {'title':	'预兆',	'year':	'2023'},
        {'title':	'年轻的心',	'year':	'2024'},
        {'title':	'捉刀人',	'year':	'2024'},
        {'title':	'哪吒之魔童闹海',	'year':	'2025'},
        {'title':	'猫猫的奇幻漂流 Straume','year':'2024'},
        {'title':	'千与千寻',	'year':	'2001'},
        {'title':	'大闹天宫',	'year':	'1961'},
        {'title':	'哪吒闹海',	'year':	'1979'},
        {'title':	'天空之城',	'year':	'1986'},
        {'title':	'龙猫',	'year':	'1988'},
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


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST': # 判断是否是 POST 请求
        title = request.form.get('title') # 获取表单数据
        year = request.form.get('year') # 获取表单数据

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('出错.') # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页

        movie = Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash('项目创建成功.') # 显示成功创建的提示

    movies = Movie.query.all()
    return render_template('index.html',movies=movies)


@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('出错.')
            return redirect(url_for('edit',movie_id=movie_id))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('项目更新成功.')
        return redirect(url_for('index'))
    return render_template('edit.html',movie=movie)

@app.route('/movie/delete/<int:movie_id>',methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id) # 获取电影记录
    db.session.delete(movie) # 删除对应的记录
    db.session.commit() # 提交数据库会话
    flash('项目删除成功.')
    db.session.commit()
    return redirect(url_for('index')) # 重定向回主页



