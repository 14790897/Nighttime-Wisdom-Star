import uuid
import requests
import json
import time
from typing import Any, List, Mapping, Optional

class AskChatGPT:

    def __init__(self):
        self.session = None
        self.parent_message_id = None

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
        response = requests.post(f"https://cloud.liuweiqing.top/api/conversation/talk", json=data)
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