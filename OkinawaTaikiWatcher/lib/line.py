import sys
import os
import requests

# prepare
url = "https://notify-api.line.me/api/notify"
access_token = os.environ.get("LINE_NOTIFY_ACCESS_TOKEN")
headers = {"Authorization": "Bearer " + access_token}

# send message


def send_line(message):
    payload = {'message': message}
    r = requests.post(url, headers=headers, params=payload,)
    print(message)
    print(r)
