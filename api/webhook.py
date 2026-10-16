from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json, requests

VERIFY_TOKEN = "momo_verify_123"
ACCESS_TOKEN = "EAAWy5YS0dxIBS8nDlgCHMd5bZAxsaqZCiQLVlCIoUsQK10RKsTAPssDZCXPjBkLbtUCTIxzxTwyVJ0I6GEnReZCFW0xgZAfznyWXQYGZAt7DA8Xzq19m1FKtBZCiHx7eMwNrqa4enzX9q8oxV8OZCf1LXeGpf8BlsUtHoHLEeDeJDy2BFkQZAhTbs6nWCaZCs9g3OEVXZCKhRdxVyBQE62ba1ZC9BF7EkQe2TBUvL0DQ6e6LcrwoCM6SbqOcTvAScmSkldknDcdSd82lFNF2feOocDk8"
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
