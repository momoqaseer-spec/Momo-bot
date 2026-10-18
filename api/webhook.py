import json
import requests

VERIFY_TOKEN = "momo123"
ACCESS_TOKEN = "EAAWy5YS0dxIBS8nDlgCHMd5bZAxsaqZCiQLVlCIoUsQK10RKsTAPssDZCXPjBkLbtUCTIxzxTwyVJ0I6GEnReZCFW0xgZAfznyWXQYGZAt7DA8Xzq19m1FKtBZCiHx7eMwNrqa4enzX9q8oxV8OZCf1LXeGpf8BlsUtHoHLEeDeJDy2BFkQZAhTbs6nWCaZCs9g3OEVXZCKhRdxVyBQE62ba1ZC9BF7EkQe2TBUvL0DQ6e6LcrwoCM6SbqOcTvAScmSkldknDcdSd82lFNF2feOocDk8"
PHONE_NUMBER_ID = "1129454846925725"

def handler(request):
    # التحقق
    if request.method == "GET":
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return (challenge, 200, {'Content-Type': 'text/plain'})
        return ('Failed', 403)

    # استقبال الرسائل
    if request.method == "POST":
        try:
            data = request.get_json()
            entry = data['entry'][0]['changes'][0]['value']
            if 'messages' in entry:
                msg = entry['messages'][0]
                from_number = msg['from']
                text_body = msg.get('text', {}).get('body', 'مرحبا')

                url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
                headers = {
                    "Authorization": f"Bearer {ACCESS_TOKEN}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "messaging_product": "whatsapp",
                    "to": from_number,
                    "text": {"body": f"أهلاً! أنا مومو شغال ✅\nرسالتك: {text_body}"}
                }
                requests.post(url, headers=headers, json=payload)
        except Exception as e:
            print(str(e))
        return ('OK', 200)
