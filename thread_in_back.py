from datetime import datetime
import schedule
import time
import random
from threading import Thread
from process import AskChatGPT
import redis

redis_url = "redis-14248.c51.ap-southeast-2-1.ec2.cloud.redislabs.com:14248"
r = redis.from_url(redis_url)
# 创建一个AskChatGPT对象
ask_chatgpt = AskChatGPT()

def process_data_job():
    while True:
        schedule.run_pending()
        time.sleep(1)

def process_data_schedule():
    if not 0 <= datetime.now().hour < 8:
        return

    for _ in range(8):  # 每三小时执行25次，about75条用户信息 in all
        time.sleep(random.uniform(5 * 60, 180 * 60 / 25))  # 随机间隔，不小于5分钟

        # with app.app_context():
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