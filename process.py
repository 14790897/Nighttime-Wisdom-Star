import os
import uuid
import requests
import json
import time
from typing import Any, List, Mapping, Optional

from dotenv import load_dotenv

#不能删除此程序新建的对话，因为会话id在此程序运行过程中会一直保留，
# 如果删除了，会话id就无法找到（新会话conversation_id应为none），造成错误
class AskChatGPT:

    def __init__(self, url):
        self.session = None
        self.parent_message_id = None
        self.url = url

    def process_data(
            self,
            prompt,
            stop=None,
            conversation_id=None,
            parent_message_id=None, ):
        # if stop is not None:
        #     raise ValueError("stop kwargs are not permitted.")
        # 将 ask_chatgpt 的逻辑放在这里
        model = "gpt-4"  # gpt-4/text-davinci-002-render-sha
        message_id = str(uuid.uuid4())
        if parent_message_id is None:
            if self.parent_message_id is not None:
                parent_message_id = self.parent_message_id
            else:
                parent_message_id = str(uuid.uuid4())
            # parent_message_id = self.parent_message_id
        if conversation_id is None and self.session is not None:
            # 默认为保存的conversation_id，也就是上一次会话，如果用户有输入，则为用户输入的id，不改变值
            conversation_id = self.session
        data = {
            "prompt": prompt,
            "model": model,
            "message_id": message_id,
            "parent_message_id": parent_message_id,
            "stream": False,
            "conversation_id": conversation_id,
        }
        response = requests.post(f"{self.url}/api/conversation/talk", json=data)
        response_data = response.text
        response_data = json.loads(response_data)
        parts = response_data['message']['content']['parts']
        # 将 parts 中的字符串连接起来形成完整的回复
        response_message = ''.join(parts)
        if stop:
            for stop_value in stop:
                stop_index = response_message.find(stop_value)
                if stop_index != -1:
                    response_message = response_message[:stop_index]
                    break
        if self.session is None:
            self.session = response_data["conversation_id"]  # 如果一开始传入的id为none，这里需要更新id
        # 更新 parent_message_id
        self.parent_message_id = response_data["message"]['id']
        return response_message

if __name__ == '__main__':
    load_dotenv()  # 加载 .env 文件
    url = os.environ.get('URL')
    ask_chatgpt = AskChatGPT(url)
    while True:
        input_data = input("请输入：")
        print(ask_chatgpt.process_data(input_data))
        time.sleep(1)