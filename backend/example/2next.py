import requests
import json, os
from dotenv import load_dotenv

try:
    load_dotenv()  # 加载 .env 文件
    token = os.environ.get("token")
    url = os.environ.get("URL")
except:
    print("请检查 .env 文件是否存在")
    exit()


payload = {
    "action": "next",
    "messages": [
        {
            "id": "aaa243c4-799e-4340-b17a-fb378626cbed",
            "author": {"role": "user"},
            "content": {"content_type": "text", "parts": ["It has been a long time since I last see you"]},
            "metadata": {},
        }
    ],
    "conversation_id": "d5f0711b-7aaa-4ded-8fdb-1d1c88e8939d",
    "parent_message_id": "a7f5bc46-9395-43b8-ab94-0332fce9a75e",
    "model": "text-davinci-002-render-sha",
    "timezone_offset_min": -480,
    "suggestions": [],
    "history_and_training_disabled": False,
    "arkose_token": None,
    "conversation_mode": {"kind": "primary_assistant"},
    "force_paragen": False,
    "force_rate_limit": False,
}
headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
response = requests.post(
    f"{url}/backend-api/conversation", headers=headers, data=json.dumps(payload)
)
print(response.text)
