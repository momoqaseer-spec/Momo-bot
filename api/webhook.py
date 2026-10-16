from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json, requests

VERIFY_TOKEN = "momo_verify_123"
ACCESS_TOKEN = "EAAWy5YS0dxIBSxNS6rdZBauPVI5JbbmfWm9w0GWmsZBnB9BmyZBUSKTO2ji7Abz3rA91AQJod8YRZBgoSxaZB1Kghp2hWFG5vS2u6DmS3UZAXNZByKGawVZACmqftiHpq8sJESCwPZBpCyB0rYaxwXURlqPZCL2Sa6c1S75n2SuTbH8Sv50QCOeS5kUXjAHh6zKE5VRaZBm9pM0JaiT9eZA3ZAkVsBP9Rm0tWKskPZB7AFoncxWMUKUrrvZAqpKaZCsLlqtL4wPHrRW2UUGexVY7dD9E2ZCYx7wZDZD"
PHONE_NUMBER_ID = "1129454846925725"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = parse_qs(urlparse(self.path).query)
        if qs.get('hub.mode',[''])[0]=='subscribe' and qs.get('hub.verify_token',[''])[0]==VERIFY_TOKEN:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(qs.get('hub.challenge',[''])[0].encode())
        else:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'no')
    def do_POST(self):
        try:
            length = int(self.headers.get('content-length',0))
            data = json.loads(self.rfile.read(length).decode())
            value = data['entry'][0]['changes'][0]['value']
            if 'messages' in value:
                msg = value['messages'][0]
                frm = msg['from']
                txt = msg.get('text',{}).get('body','')
                url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
                headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type":"application/json"}
                payload = {"messaging_product":"whatsapp","to":frm,"type":"text","text":{"body":f"أهلاً! وصلتني رسالتك: {txt}\nمومو شغال ✅"}}
                requests.post(url, headers=headers, json=payload)
        except Exception as e:
            print(e)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')
