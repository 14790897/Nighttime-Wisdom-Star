# -*- coding: utf-8 -*-
import os
import uuid
import requests
import json
import time
import logging

from dotenv import load_dotenv


# 不能删除此程序新建的对话，因为会话id在此程序运行过程中会一直保留，
# 如果删除了，会话id就无法找到（新会话conversation_id应为none），造成错误
class AskChatGPT:
    def __init__(self, url, headers):
        self.session = None
        self.parent_message_id = None
        self.url = url
        self.headers = headers

    def pre_process(self, data_lines):
        parsed_data_list = []  # 用于存储解析后的数据

        # 将单个字符串分割为多行
        lines = data_lines.splitlines()
        for line in lines:
            try:
                if line.startswith("data: "):
                    json_data = line.split(" ", 1)[1]
                    try:
                        parsed_data = json.loads(json_data)
                        parsed_data_list.append(parsed_data)  # 添加到列表中
                    except json.JSONDecodeError:
                        print("无法解析的 JSON 数据:", json_data)
                else:
                    # print("不是 JSON 数据的行:", line)
                    pass
            except Exception as e:  # 捕获更广泛的异常
                print("解析错误:", e)

        # 检查列表是否有足够的数据
        if len(parsed_data_list) >= 3:
            print("返回的完整数据：", parsed_data_list[-3])
            return parsed_data_list[-3]  # 返回倒数第三个元素
        else:
            return None  # 没有足够的数据返回 None

    def process_data(
        self,
        prompt,
        stop=None,
        conversation_id=None,
        parent_message_id=None,
    ):
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
        if conversation_id is None and self.session is not None:
            # 默认为保存的conversation_id，也就是上一次会话，如果用户有输入，则为用户输入的id，不改变值
            conversation_id = self.session
        data = {
            "action": "next",
            "messages": [
                {
                    "id": message_id,
                    "author": {"role": "user"},
                    "content": {"content_type": "text", "parts": [prompt]},
                    "metadata": {},
                }
            ],
            "conversation_id": conversation_id,
            "message_id": message_id,
            "parent_message_id": parent_message_id,
            "model": model,
            "timezone_offset_min": -480,
            "suggestions": [],
            "history_and_training_disabled": False,
            "arkose_token": None,
            "conversation_mode": {"kind": "primary_assistant"},
            "force_paragen": False,
            "force_rate_limit": False,
        }

        response = requests.post(
            f"{self.url}/backend-api/conversation", json=data, headers=self.headers
        )
        if response.status_code not in range(200, 300):
            logging.error(
                f"API call failed with status {response.status_code}: {response.text}"
            )
            return json.dumps({"error": f"API call failed: {response.text}"})
        try:
            response_data = self.pre_process(response.text)  # 新的预处理
            # response_data = json.loads(response_data)  # 尝试解析数据
            parts = response_data["message"]["content"]["parts"]
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON data: {response_data}")
            response_data = json.dumps(
                {"error": "Invalid data received, Jsondecodererror"}
            )  # 创建一个错误的 JSON 响应
            return response_data
        except TypeError:
            logging.error(f"Invalid JSON data: {response_data}")
            response_data = json.dumps({"error": "Invalid data received, type error"})
            return response_data
        # 将 parts 中的字符串连接起来形成完整的回复
        response_message = "".join(parts)
        if stop:
            for stop_value in stop:
                stop_index = response_message.find(stop_value)
                if stop_index != -1:
                    response_message = response_message[:stop_index]
                    break
        if self.session is None:
            self.session = response_data["conversation_id"]  # 如果一开始传入的id为none，这里需要更新id
        # 更新 parent_message_id
        self.parent_message_id = response_data["message"]["id"]
        return response_message


if __name__ == "__main__":
    load_dotenv()  # 加载 .env 文件
    token = os.environ.get("PANDORA_ACCESS_TOKEN")
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    url = os.environ.get("URL")
    ask_chatgpt = AskChatGPT(url, headers)
    while True:
        input_data = input("请输入：")
        print(ask_chatgpt.process_data(input_data))
        time.sleep(1)
