import requests

url = "https://ai.fakeopen.com/token/register"

payload = "unique_name=fakeopen&access_token=.......&site_limit=https%3A%2F%2Fchat.xf233.com&expires_in=0&show_conversations=true&show_userinfo=true"
headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
