from datetime import datetime, timedelta, time as dt_time
from multiprocessing import Process

from pytz import timezone
import pytz
import time
import random
import redis
import os
from process import AskChatGPT
from dotenv import load_dotenv
import logging
import sys
from celery import Celery
from threading import Thread

#连接远程redis
password = os.environ.get('REDIS_PASSWORD')
try:
    r = redis.StrictRedis(
        host='localhost',
        port=6379,
        password=password,  # 使用环境变量中的密码
        db=0,
        decode_responses=True
    )
except Exception as e:
    print(f"Error while connecting to Redis: {e}")
    exit(1)
    
# 创建一个AskChatGPT对象
try:
    load_dotenv()  # 加载 .env 文件
    url = os.environ.get('URL')
except Exception as e:
    print(f"Error while loading .env file: {e}")
    exit(1)
ask_chatgpt = AskChatGPT(url)

def process_data_schedule():
    if not 0 <= datetime.now(pytz.timezone('Asia/Shanghai')).hour < 8:
        return
    
    time_count = 0

    for i in range(60):  # 每三小时执行20次，共60条左右的用户信息
        sleep_time = random.uniform(2 * 60, 180 * 60 / 20)
        # sleep_time = 2
        print(f"sleep_time: {sleep_time}")
        time.sleep(sleep_time)  # 随机间隔，不小于5分钟
        time_count += sleep_time
        data_keys = r.keys(pattern="*:data")
        for data_key in data_keys:
            username = data_key[:-5]
            result_key = f"{username}:results"
            counter_key = f"{username}:counter"
            error_key = f"{username}:errors"  # 新增错误信息键
            input_data = r.lpop(data_key)
            # processed_count = r.llen(result_key)
            # 获取当前用户已处理的输入数量
            processed_count = int(r.get(counter_key) or 0)

            if input_data:
                if processed_count < 10:
                    try:
                        # try:
                        print(f"Input data: {input_data}")
                        result = ask_chatgpt.process_data(input_data)
                        # result = "我爱你"
                        print(f"Result: {result}")
                        # except json.JSONDecodeError as e:
                            # print(f"Error while decoding JSON data: {e}")
                            # 处理错误，例如使用默认值或记录错误信息
                        # 拼接输入和输出字符串，并一起存入 Redis
                        history_entry = f"输入：{input_data} 输出：{result}"
                        r.lpush(result_key, history_entry)
                        # 更新计数器
                        r.incr(counter_key)
                        # 设置计数器每日到期
                        # r.expireat(counter_key, datetime.combine(datetime.now().date() + timedelta(days=1), time.min))
                        # 创建北京时间的时区对象
                        beijing_tz = timezone('Asia/Shanghai')
                        now_beijing = datetime.now(beijing_tz)
                        tomorrow_midnight_beijing = beijing_tz.localize(
                            datetime.combine(now_beijing.date() + timedelta(days=1), dt_time.min))
                        # 设置过期时间
                        r.expireat(counter_key, tomorrow_midnight_beijing)
                    except Exception as e:
                        print(e)
                        #给用户展示
                        error_entry = f"I'm so sorry, there is an error. If you have any questions, please contact the administrator."
                        #给管理员查看
                        error_message = f"There is an error: {str(e)}."
                        r.lpush(result_key, error_entry)
                        r.lpush(error_key, error_message)  # 将错误信息存储在专门的错误信息键中
                else:
                    error_entry = f"输入已达上限（5个），无法继续处理。如需帮助，请联系管理员。"
                    r.lpush(result_key, error_entry)
        if (i+1) % 20 == 0:
            if time_count < 180*60:
                time.sleep(180*60 - time_count)
                time_count = 0

def process_loop():
    while True:
        process_data_schedule()


if __name__ == '__main__':
    p = Process(target=process_loop)
    p.start()
    p.join()
# 创建一个后台线程，运行定时任务
# thread = Thread(target=process_data_schedule)
# thread.start()