#import eventlet
#eventlet.monkey_patch()
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
import redis
from flask import session, request, jsonify
from flask import send_from_directory
from flask_socketio import SocketIO, emit, join_room
from flask_seasurf import SeaSurf
import os, json
from flask_cors import CORS
from dotenv import load_dotenv
import logging
import sys
sys.path.insert(0, '.')
# from celery_config import app as celery_app

from process import AskChatGPT
import logging
import threading

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
    logger.info(f"Error while loading .env file: {e}")
    exit(1)

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
        static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

CORS(app, resources={r'/*': {'origins': '*', 'supports_credentials': True}})
socketio = SocketIO(app, cors_allowed_origins='*',)#async_mode='eventlet')
# print('secret_key', secret_key)
app.config['SECRET_KEY'] = secret_key
app.secret_key = os.environ.get('SECRET_KEY')#linux必须用这行代码5.11
app.permanent_session_lifetime = timedelta(minutes=6000)  # Set session lifetime to 5 minutes
# app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# csrf = SeaSurf(app)

redis_host = os.getenv('REDIS_HOST', 'localhost')
try:
    r = redis.StrictRedis(
            host=redis_host,#'redis','localhost'
            port=6379,
            db=0,
            decode_responses=True
            )
except Exception as e:
    logger.info(f"Error while connecting to Redis: {e}")
    exit(1)


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    logger.info(f"Received username: {username}")  # 打印接收到的用户名
    logger.info(f"Received password: {password}")  # 打印接收到的密码
    if r.exists(username) and r.get(username) == password:
        session.permanent = True
        session['username'] = username
        print('session/login', session)
        # Emit a 'login_success' event. 这是触发加入room的第一步
        # socketio.emit('login_success', {'username': username})
        # join_room(username)只能在websocket请求中使用6.1
        return {'status': 'success'}, 200
    else:
        return {'status': 'failed', 'message': 'Login failed. Check your username and password.'}, 401

    
@socketio.on('home_ready')
def handle_home_ready():
    if session.get('username'):
        socketio.emit('login_success')

@socketio.on('join')
def on_join():
    # username = data['username']
    username = session['username']
    # Use the username as the name of the room.
    print('----------------------------------------------------------join--------', username)
    join_room(username)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not r.exists(username):
        r.set(username, password)
        session['username'] = username
        return jsonify({'status': 'success', 'message': 'Account created successfully. You can now log in.'})
    else:
        return jsonify({'status': 'fail', 'message': 'Username already exists. Choose a different one.'})


@app.route('/api/home', methods=['POST'])
def home_post():
    print('session/home', session)
    if request.is_json:
        if 'username' in session:
            username = session['username']
            data_key = f"{username}:data"
            data = request.get_json()
            input_data = data.get('input_data')  # 获取 input_data 字段的值
            # 将数据添加到Redis中的对应项
            r.lpush(data_key, input_data)
            # flash('Data submitted successfully.', 'success')
            return jsonify(success=True, message='Data submitted successfully.')
        else:
            return jsonify(success=False, message='Please log in to submit data.'), 403
    else:
        return jsonify(success=False, message='Request is not JSON.'), 400

@app.route('/api/history', methods=['GET'])
def history():
    chat_history = []
    print('session/api/history', session)
    if 'username' in session:
        username = session['username']
        result_key = f"{username}:results"
        history = r.lrange(result_key, 0, -1)[::-1]
        if not history:
            return jsonify(history=chat_history)
        chat_history = get_chat_history(history,username)
        return jsonify(history=chat_history)
    else:
        return jsonify(message="用户未登录"), 401  # 401 是未授权的 HTTP 状态码  , csrf_token=csrf._get_token()

# @app.route('/api/csrf-token', methods=['GET'])
# def get_csrf_token():
#     return jsonify(token=csrf._get_token())


def get_chat_history(raw_data,username):
    chat_history = []
    data_key = f"{username}:data"
    raw_data.extend(r.lrange(data_key, 0, -1)[::-1])
    for message in raw_data:
        split_message = message.split(',')
        if len(split_message) > 1:
            for message in split_message:
                print('message', message)
                try:
                    message = message.split(':')
                    text = message[1].strip()
                except:
                    text = message
                sender = 'me' if 'input' in message[0] else 'bot'
                chat_history.append({'text': text, 'sender': sender})
        else:
            logger.info(f"split_message = {split_message}")
            print('split_message',split_message)
            try:
                #以前的输入可能有问题
                chat_history.append({'text': split_message[0].split(':')[1].strip(), 'sender': 'me'})
            except:
                chat_history.append({'text': split_message[0], 'sender': 'me'})
    print('chat_history',chat_history)
    return chat_history

counts = -1
@app.route('/api/receive_message', methods=['POST'])
def receive_message():
    message_data = request.get_json()
    username = message_data['username']
    logger.info('-----message-room------', username)
    socketio.emit('result', {'data': message_data}, room=username)
    logger.info('socketio结果信息已发送')
    global counts 
    counts = message_data.get('remain_counts', counts)
    return '', 200  # 添加这一行代码，返回状态码200

@app.route('/api/available_chats', methods=['GET'])
def available_chats():
    if counts == -1:
        default_value = os.environ.get('amount')
        if default_value is None:
            default_value = "0"  # or some other default value
        return jsonify(availableChats=default_value)
    else:
        return jsonify(availableChats=counts)
    
@app.route('/api/init_chat', methods=['GET'])
def init_chat():
    return jsonify(start_time=os.environ.get('start_time'), end_time=os.environ.get('end_time'), availableChats=r.get)
    
    
if __name__ == '__main__':
    debug = os.environ.get("ENV") == "development"
    socketio.run(app, host='0.0.0.0', port=5000, debug=debug)
    # app.run(host='0.0.0.0', port=5000, debug=debug)
