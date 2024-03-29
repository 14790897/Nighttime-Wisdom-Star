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
import sys, json, requests
from threading import Thread
from flask_socketio import SocketIO, emit

# 创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # 设置日志级别
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler("output_process.log")
fh.setLevel(logging.INFO)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# 定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)

# 记录一条日志
logger.info("hello, logger, start logs")

instant_reply = False

# socketio = SocketIO(app)


try:
    load_dotenv()  # 加载 .env 文件
    url = os.environ.get("URL")
    redis_host = os.getenv("REDIS_HOST", "localhost")
except Exception as e:
    logger.info(f"Error while loading .env file: {e}")
    exit(1)
try:
    r = redis.StrictRedis(
        host=redis_host, port=6379, db=0, decode_responses=True  #'redis','localhost'
    )
except Exception as e:
    logger.info(f"Error while connecting to Redis: {e}")
    exit(1)
    # 创建一个AskChatGPT对象
token = os.environ.get("PANDORA_ACCESS_TOKEN")
headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
ask_chatgpt = AskChatGPT(url, headers)


def process_data_schedule(instant_reply, enable_wait_time):
    # logger.info(f"process_data_schedule 函数被调用，instant_reply = {instant_reply}")
    # logging.info("进入 process_data_schedule 函数")
    current_hour = datetime.now(pytz.timezone(os.environ.get("time_zone"))).hour
    start_time = int(os.environ.get("start_time"))
    end_time = int(os.environ.get("end_time"))

    process_counter_key = "process_counter"  # 新建处理计数键
    r.set(process_counter_key, 0)  # 初始化处理计数键

    if not instant_reply:
        if start_time < end_time:
            if not start_time <= current_hour < end_time:
                return
        else:  # 当 'start_time' >= 'end_time'，考虑时间跨越午夜的情况
            if end_time <= current_hour <= start_time:
                return
    time_count = 0
    remain_counts_key = "remain_counts"  # 新建剩余次数键6.6
    r.set(remain_counts_key, int(os.environ.get("amount")))  # 初始化剩余次数6.6

    # for i in range(int(os.environ.get('amount'))):  # 每三小时执行25次，共75条左右的用户信息
    while int(r.get(remain_counts_key)) > 0:  # 当剩余次数大于0时，继续执行
        if not instant_reply:
            if enable_wait_time:
                # todo 这里加个可以选择休息时间的选项6.16
                sleep_time = random.uniform(2 * 60, 180 * 60 / 20)
                # 将睡眠时间变短 6.7
                # sleep_time = 10
                logger.info(f"sleep_time: {sleep_time}")
                time.sleep(sleep_time)  # 随机间隔，不小于5分钟
                time_count += sleep_time
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
                if processed_count < 200:
                    try:
                        logger.info(f"Input data: {input_data}")
                        # 读取列表的所有元素
                        all_items = r.lrange(result_key, 0, -1)
                        # 反转列表以获取时间顺序的数据（最早的数据在前）
                        all_items.reverse()

                        # 拼接所有元素
                        combined_data = "".join(item for item in all_items)
                        shortened_data = combined_data[-5000:]
                        input_data_with_history = (
                            f"history:{shortened_data}+user input:{input_data}"
                        )
                        result = call_api_with_retry(
                            lambda: ask_chatgpt.process_data(input_data_with_history)
                        )
                        logger.info(f"Result: {result}")

                        r.incr(process_counter_key)  # 处理计数加一

                        # socketio.emit('result', {'text1': result,  'sender': 'bot', 'text2':input_data, 'sender2': 'me'})
                        # 拼接输入和输出字符串，并一起存入 Redis
                        history_entry = f"input:{input_data}, output:{result}"
                        r.lpush(result_key, history_entry)
                        remaining_counts = (
                            int(os.environ.get("amount")) - processed_count - 1
                        )  # 计算剩余次数
                        r.set(remain_counts_key, remaining_counts)  # 将剩余次数存入 Redis

                        data = {
                            "username": username,
                            "input": input_data,
                            "output": result,
                            "remain_counts": remaining_counts,
                        }
                        response = requests.post(
                            "http://localhost:5001/api/receive_message", json=data
                        )
                        # 更新计数器
                        r.incr(counter_key)
                        # 创建北京时间的时区对象
                        beijing_tz = timezone(os.environ.get("time_zone"))
                        now_beijing = datetime.now(beijing_tz)
                        tomorrow_midnight_beijing = beijing_tz.localize(
                            datetime.combine(
                                now_beijing.date() + timedelta(days=1), dt_time.min
                            )
                        )
                        # 设置过期时间
                        r.expireat(counter_key, tomorrow_midnight_beijing)
                    except Exception as e:
                        logger.info(e)
                        # 给用户展示
                        error_entry = f"I'm so sorry, there is an error. If you have any questions, please contact the administrator.{str(e)}"
                        # 给管理员查看
                        error_message = f"There is an error: {str(e)}."
                        r.lpush(result_key, error_entry)
                        r.lpush(error_key, error_message)  # 将错误信息存储在专门的错误信息键中
                else:
                    error_entry = f"输入已达上限（100个），无法继续处理。如需帮助，请联系管理员。"
                    r.lpush(result_key, error_entry)
        if (
            not instant_reply
            and int(r.get(process_counter_key)) != 0
            and int(r.get(process_counter_key)) % 25 == 0
        ):
            response = requests.get("http://localhost:5001/api/limit_warning")
            if enable_wait_time:
                if time_count < 180 * 60:
                    time.sleep(180 * 60 - time_count)
                    time_count = 0
        else:
            time.sleep(5)
        # logger.info(msg=f"第{i+1}次循环结束")
        # logger.info(msg=f'进程id: {os.getpid()}')
    logger.info("退出 process_data_schedule 函数")


def process_loop(instant_reply, enable_wait_time):
    while True:
        process_data_schedule(instant_reply, enable_wait_time)


def call_api_with_retry(api_function, max_retries=5):
    for i in range(max_retries):
        try:
            return api_function()
        except Exception as e:
            if i < max_retries - 1:  # i 从0开始，所以这里需要 -1
                sleep_time = (2**i) + random.random()  # 指数退避 + 随机化
                time.sleep(sleep_time)
            else:
                logger.info(f"请求ChatGPT过程中出现异常:{e}")


if __name__ == "__main__":
    instant_reply = os.environ.get("ENV") == "development"
    # enable_wait_time = os.environ.get("ENABLE_WAIT_TIME", "False") == "True"
    enable_wait_time=False
    p = Process(target=process_loop, args=(instant_reply, enable_wait_time))
    p.start()
