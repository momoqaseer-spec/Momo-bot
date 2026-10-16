from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

VERIFY_TOKEN = "momo_verify_123"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        mode = qs.get('hub.mode', [''])[0]
        token = qs.get('hub.verify_token', [''])[0]
        challenge = qs.get('hub.challenge', [''])[0]
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(challenge.encode())
        else:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'Forbidden')
    
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')
