from datetime import datetime, timedelta, time as dt_time
from pytz import timezone
import pytz
import time
import random
from threading import Thread
from flask import Flask, render_template, redirect, url_for, flash, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
import redis
from flask import session
import os
from process import AskChatGPT
from dotenv import load_dotenv
import logging
import sys
sys.path.insert(0, '.')
from celery_config import app as celery_app


try:
    load_dotenv()  # 加载 .env 文件
    url = os.environ.get('URL')
    secret_key = os.environ.get('SECRET_KEY')
except Exception as e:
    print(f"Error while loading .env file: {e}")
    exit(1)
# 创建一个AskChatGPT对象
ask_chatgpt = AskChatGPT(url)
# 生成一个256位的随机密钥
# secret_key = secrets.token_hex(32)
# print("secret_key",secret_key)
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
app.config['SECRET_KEY'] = secret_key
app.secret_key = os.environ.get('SECRET_KEY')#linux必须用这行代码5.11

handler = logging.FileHandler('flask.log')  # errors are logged to this file
handler.setLevel(logging.ERROR)  # only log errors and above
app.logger.addHandler(handler)  # attach the handler to the app's logger

# 获取 Redis 连接字符串并创建连接
# redis_url = os.environ.get('REDIS_URL')
# r = redis.from_url(redis_url)

# 创建Redis连接
host = os.environ.get('REDIS_HOST')
password = os.environ.get('REDIS_PASSWORD')

try:
    r = redis.StrictRedis(
        host='your-redis-host',
        port=6379,
        password=password,  # 使用环境变量中的密码
        db=0,
        decode_responses=True
    )
except Exception as e:
    print(f"Error while connecting to Redis: {e}")
    exit(1)


# 登录表单
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# 注册表单
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class DataForm(FlaskForm):
    input_data = StringField('Input Data', validators=[DataRequired()])
    submit = SubmitField('Send Data')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if r.exists(form.username.data) and r.get(form.username.data) == form.password.data:
            flash('Logged in successfully.', 'success')
            session['username'] = form.username.data
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not r.exists(form.username.data):
            r.set(form.username.data, form.password.data)
            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Choose a different one.', 'danger')
    return render_template('register.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = DataForm()
    history = []
    if form.validate_on_submit():
        input_data = form.input_data.data
        if 'username' in session:
            username = session['username']
            data_key = f"{username}:data"
            # 将数据添加到Redis中的对应项
            r.lpush(data_key, input_data)
            flash('Data submitted successfully.', 'success')
            form = DataForm()  # 重新初始化表单，清空字段
            return redirect(url_for('home'))  # 重定向到新的页面
    if 'username' in session:
        username = session['username']
        result_key = f"{username}:results"
        history = r.lrange(result_key, 0, -1)
    else:
        flash('Please log in to submit data.', 'warning')
    return render_template('home.html', form=form, history=history)


if __name__ == '__main__':
    # if os.environ.get("ENV") == "development":
    app.run(host='127.0.0.1', port=5000, debug=True)
    # process_data_schedule.delay()
