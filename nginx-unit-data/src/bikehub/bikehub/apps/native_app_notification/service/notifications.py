import requests
import json

class Notifications():
    def send_notification(self,token,title,body,data):
        target_url = 'https://exp.host/--/api/v2/push/send'
        headers = {
            'Accept': 'application/json',
            'Accept-encoding': 'gzip, deflate',
            'Content-Type': 'application/json',
        }

        data={
            "to":token,
            "sound":"default",
            "title":title,
            "body":body,
            'data':data,
        }

        r = requests.post(
            target_url,
            data=json.dumps(data),
            headers=headers
            )
        
        # print(r.text)
        # print(r.status_code)