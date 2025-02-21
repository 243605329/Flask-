from flask import Flask,url_for

app = Flask(__name__)

@app.route('/')
def hello():
    return	'<h1>Hello	Totoro!</h1><img	src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    return	'<h1>Hello,	{name}!</h1>'

@app.route('/test')
def test_url_for():
    print(url_for('hello')) # 输出：/
    print(url_for('user_page', name='greyli')) # 输出：/user/greyli
    print(url_for('user_page', name='peter')) # 输出：/user/peter
    print(url_for('test_url_for')) # 输出：/test
    print(url_for('test_url_for',num=2)) # 输出：/test?num=2
    return	f'<h1>Test	page</h1> <p>{url_for('test_url_for')}<p>'


