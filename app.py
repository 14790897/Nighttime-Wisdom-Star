from datetime import datetime, timedelta, time as dt_time
from multiprocessing import Process
from pytz import timezone
import pytz
import schedule
import time
import random
from threading import Thread
from flask import Flask, render_template, redirect, url_for, flash, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo
import redis
from flask import session
import os
from process import AskChatGPT
from dotenv import load_dotenv
import logging
import sys
sys.path.insert(0, '.')
# from celery_config import app as celery_app
import logging

# logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

# 创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # 设置日志级别
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('output.log')
fh.setLevel(logging.INFO)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)

# 记录一条日志
logger.info('hello, logger, start logs')

instant_reply = False


try:
    load_dotenv()  # 加载 .env 文件
    url = os.environ.get('URL')
    secret_key = os.environ.get('SECRET_KEY')
except Exception as e:
    logger(f"Error while loading .env file: {e}")
    exit(1)
# 创建一个AskChatGPT对象
ask_chatgpt = AskChatGPT(url)
# 生成一个256位的随机密钥
# secret_key = secrets.token_hex(32)
# print("secret_key",secret_key)
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
app.config['SECRET_KEY'] = secret_key
app.secret_key = os.environ.get('SECRET_KEY')#linux必须用这行代码5.11

# handler = logging.FileHandler('flask.log')  # errors are logged to this file
# handler.setLevel(logging.ERROR)  # only log errors and above
# app.logger.addHandler(handler)  # attach the handler to the app's logger

redis_host = os.getenv('REDIS_HOST', 'localhost')
try:
    r = redis.StrictRedis(
        host=redis_host,#'redis','localhost'
        port=6379,
        db=0,
        decode_responses=True
    )
except Exception as e:
    logger(f"Error while connecting to Redis: {e}")
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
    input_data = TextAreaField('Input Data', validators=[DataRequired()])
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
    chat_history = []
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
        history = r.lrange(result_key, 0, -1)[::-1]
        chat_history = get_chat_history(history)
    else:
        flash('Please log in to submit data.', 'warning')
    return render_template('home.html', form=form, history=chat_history)

def get_chat_history(raw_data):
    chat_history = []
    for message in raw_data:
        split_message = message.split(',')
        if len(split_message) > 1:
            for message in split_message:
                print('message',message)
                try:
                    message = message.split(':')
                    text = message[1].strip()
                except:
                    text = message
                sender = 'me' if 'input' in message[0] else 'bot'
                chat_history.append({'text': text, 'sender': sender})
        else:
            chat_history.append({'text': split_message[0].split(':')[1], 'sender': 'me'})
    return chat_history

# @app.after_request
# def add_header(response):
#     if os.environ.get("ENV") == "development":
#         response.cache_control.no_cache = True
#         return response

#app.py
# @celery_app.task
#此进程和flask同时运行只适合本地调试使用，所以这里并没有调用处理进程，
# 这部分处理输入的代码已经全部放在progress_in_back.py中，两个python代码分开运行
def process_data_schedule(instant_reply):
    logger.info(f"process_data_schedule 函数被调用，instant_reply = {instant_reply}")
    # logging.info("进入 process_data_schedule 函数")
    if not instant_reply and not 0 <= datetime.now(pytz.timezone('Asia/Shanghai')).hour < 8:
        return
    
    time_count = 0

    for i in range(60):  # 每三小时执行20次，共60条左右的用户信息
        if not instant_reply:
            sleep_time = random.uniform(2 * 60, 180 * 60 / 20)
            # sleep_time = 2
            logger.info(f"sleep_time: {sleep_time}")
            time.sleep(sleep_time)  # 随机间隔，不小于5分钟
            time_count += sleep_time
        with app.app_context():
            data_keys = r.keys(pattern="*:data")
            for data_key in data_keys:
                username = data_key[:-5]
                result_key = f"{username}:results"
                counter_key = f"{username}:counter"
                error_key = f"{username}:errors"  # 新增错误信息键
                input_data = r.rpop(data_key)
                # processed_count = r.llen(result_key)
                # 获取当前用户已处理的输入数量
                processed_count = int(r.get(counter_key) or 0)

                if input_data:
                    if processed_count < 100: #这是每个人的提问次数，现在是每个人每天可发送100条消息
                        try:
                            logger.info(f"Input data: {input_data}")
                            result = call_api_with_retry(lambda: ask_chatgpt.process_data(input_data))
                            logger.info(f"Result: {result}")
                            # 拼接输入和输出字符串，并一起存入 Redis
                            history_entry = f"input:{input_data}, output:{result}"
                            r.lpush(result_key, history_entry)
                            # 更新计数器
                            r.incr(counter_key)
                            # 创建北京时间的时区对象
                            beijing_tz = timezone('Asia/Shanghai')
                            now_beijing = datetime.now(beijing_tz)
                            tomorrow_midnight_beijing = beijing_tz.localize(
                                datetime.combine(now_beijing.date() + timedelta(days=1), dt_time.min))
                            # 设置过期时间
                            r.expireat(counter_key, tomorrow_midnight_beijing)
                        except Exception as e:
                            logger.info(e)
                            #给用户展示
                            error_entry = f"I'm so sorry, there is an error. If you have any questions, please contact the administrator."
                            #给管理员查看
                            error_message = f"There is an error: {str(e)}."
                            r.lpush(result_key, error_entry)
                            r.lpush(error_key, error_message)  # 将错误信息存储在专门的错误信息键中
                    else:
                        error_entry = f"输入已达上限（10个），无法继续处理。如需帮助，请联系管理员。"
                        r.lpush(result_key, error_entry)
        if not instant_reply and (i+1) % 20 == 0:
            if time_count < 180*60:
                time.sleep(180*60 - time_count)
                time_count = 0
        else:
            time.sleep(5)
        logger.info(msg=f"第{i+1}次循环结束")
        print('进程id', os.getpid())
        logger.info(f'进程id: {os.getpid()}')
    logger.info("退出 process_data_schedule 函数")
    
def process_loop(instant_reply):
    while True:
        process_data_schedule(instant_reply)
    
# thread = Thread(target=process_data_schedule)
# thread.start()

def call_api_with_retry(api_function, max_retries=5):
    for i in range(max_retries):
        try:
            return api_function()
        except Exception as e:
            if i < max_retries - 1:  # i 从0开始，所以这里需要 -1
                sleep_time = (2 ** i) + random.random()  # 指数退避 + 随机化
                time.sleep(sleep_time)
            else:
                raise


if __name__ == '__main__':
    instant_reply = os.environ.get("ENV") == "development"
    #此进程只适合本地调试使用，所以这部分处理输入的代码已经全部放在progress_in_back.py中，两个python代码分开运行
    progress_run =  os.environ.get("ENV") == "development"
    if progress_run:
        p = Process(target=process_loop, args=(instant_reply,))
        p.start()
    debug = os.environ.get("ENV") == "development"
    app.run(host='0.0.0.0', port=5000, debug=debug)
    # p.join()