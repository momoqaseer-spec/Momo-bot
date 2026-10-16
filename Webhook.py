from http.server import BaseHTTPRequestHandler
import json, os, requests

VERIFY_TOKEN = "momo_verify_123"
ACCESS_TOKEN = "EAAWy5YS0dxIBSxNS6rdZBauPVI5JbbmfWm9w0GWmsZBnB9BmyZBUSKTO2ji7Abz3rA91AQJod8YRZBgoSxaZB1Kghp2hWFG5vS2u6DmS3UZAXNZByKGawVZACmqftiHpq8sJESCwPZBpCyB0rYaxwXURlqPZCL2Sa6c1S75n2SuTbH8Sv50QCOeS5kUXjAHh6zKE5VRaZBm9pM0JaiT9eZA3ZAkVsBP9Rm0tWKskPZB7AFoncxWMUKUrrvZAqpKaZCsLlqtL4wPHrRW2UUGexVY7dD9E2ZCYx7wZDZD"
PHONE_NUMBER_ID = "1129454846925725"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if "hub.mode=subscribe" in self.path and f"hub.verify_token={VERIFY_TOKEN}" in self.path:
            from urllib.parse import parse_qs, urlparse
            query = parse_qs(urlparse(self.path).query)
            challenge = query.get('hub.challenge', [''])[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(challenge.encode())
        else:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'Verification failed')

    def do_POST(self):
        length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(length).decode()
        try:
            data = json.loads(body)
            value = data['entry'][0]['changes'][0]['value']
            if 'messages' in value:
                msg = value['messages'][0]
                num = msg['from']
                txt = msg.get('text', {}).get('body','')
                url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
                requests.post(url, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}, json={"messaging_product":"whatsapp","to":num,"type":"text","text":{"body":f"وصلتني: {txt} - مومو شغال ✅"}})
        except: pass
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')
