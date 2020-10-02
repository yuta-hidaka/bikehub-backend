import requests
import json


class Notifications():
    def send_notification(self, token, target_url, title, body, data):
        headers = {
            'Accept': 'application/json',
            'Accept-encoding': 'gzip, deflate',
            'Content-Type': 'application/json',
        }

        data = {
            "to": token,
            "sound": "default",
            "title": title,
            "body": body,
            'data': data,
        }

        r = False

        try:
            r = requests.post(
                target_url,
                data=json.dumps(data),
                headers=headers
            )
            print(r.text)
        except Exception as e:
            print(e)

        return r
