import requests, os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件
token = os.environ.get("PANDORA_ACCESS_TOKEN")

url = "https://ai.fakeopen.com/token/register"

payload = f"unique_name=fakeopen&access_token={token}&expires_in=0&show_conversations=true&show_userinfo=true"
headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
