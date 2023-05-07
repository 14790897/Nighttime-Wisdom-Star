from datetime import datetime

import schedule
import time
import random
from threading import Thread
from flask import Flask, render_template, redirect, url_for, flash, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
import redis
import os
import secrets
from flask import session
from flask import request
import os
from process import AskChatGPT

# 创建一个AskChatGPT对象
ask_chatgpt = AskChatGPT()
# 生成一个256位的随机密钥
# secret_key = secrets.token_hex(32)
secret_key = os.environ.get('SECRET_KEY')
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
app.config['SECRET_KEY'] = secret_key

# 获取 Redis 连接字符串并创建连接
redis_url = os.environ.get('REDIS_URL')
r = redis.from_url(redis_url)

# 创建Redis连接
# r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

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
    if 'username' in session:
        username = session['username']
        result_key = f"{username}:results"
        history = r.lrange(result_key, 0, -1)
    else:
        flash('Please log in to submit data.', 'warning')
    return render_template('home.html', form=form, history=history)


# @app.route('/submit_data', methods=['POST'])
# def submit_data():
#     input_data = request.form['input_data']
#
#     # 在这里处理用户数据，例如：
#     result = process_data(input_data)
#
#     # 将结果发送回客户端
#     return result


def process_data_job():
    while True:
        schedule.run_pending()
        time.sleep(1)

def process_data_schedule():
    if not 0 <= datetime.now().hour < 8:
        return

    for _ in range(8):  # 每三小时执行25次，about75条用户信息 in all
        time.sleep(random.uniform(5 * 60, 180 * 60 / 25))  # 随机间隔，不小于5分钟

        with app.app_context():
            data_keys = r.keys(pattern="*:data")
            for data_key in data_keys:
                username = data_key[:-5]
                result_key = f"{username}:results"
                input_data = r.lpop(data_key)
                if input_data:
                    try:
                        result = ask_chatgpt.process_data(input_data)
                        r.lpush(result_key, result)
                    except Exception as e:
                        print(e)
                        r.lpush(result_key, "I'm so sorry, there is an error: " + str(e) +
                                "If you have any questions, please contact the administrator.")

schedule.every().day.at("00:00").do(process_data_schedule)

# 创建一个后台线程，运行定时任务
thread = Thread(target=process_data_job)
thread.start()



if __name__ == '__main__':
    # if os.environ.get("ENV") == "development":
    app.run(debug=True)

