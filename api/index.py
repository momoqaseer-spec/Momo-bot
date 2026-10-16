from http.server import BaseHTTPRequestHandler
import json, os, requests

VERIFY_TOKEN = "momo_verify_123"
ACCESS_TOKEN = "EAAQgviMB0eEBSrZBZCynBcGxXkEQ4LQM065bRwd7a7x4Y33FUpG3sJc6Oj1GZAoQ86QAP7mEPJsMZBBO290TgoNHpAM38A4u0zjwXI5SvONRP75Fq1UCVcKUP0yZBsL489epJlo7BF10AXROu5bhnUFbiasNOonmFJ9vLSxcz15cMJ9Ai6ZCP02hydNKJUtyFV35cwGumhM4oh2ZBkOOiqLJGtLILCLtyrsrZBNk6gZDZD"
PHONE_NUMBER_ID = "128397081476514"

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
