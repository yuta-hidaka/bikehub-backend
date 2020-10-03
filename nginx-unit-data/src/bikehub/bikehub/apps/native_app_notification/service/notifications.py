import requests
import json
from concurrent.futures import ThreadPoolExecutor


class Notifications():
    def send_notification(self, tokens, target_url, title, body, data):
        headers = {
            'Accept': 'application/json',
            'Accept-encoding': 'gzip, deflate',
            'Content-Type': 'application/json',
        }

        data = {
            "to": tokens,
            "sound": "default",
            "title": title,
            "body": body,
            'data': data,
        }

        try:
            return requests.post(
                target_url,
                data=json.dumps(data),
                headers=headers
            )
        except Exception as e:
            print(e)
            return None
