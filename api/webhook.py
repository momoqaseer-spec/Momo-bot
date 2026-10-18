import json
import requests

VERIFY_TOKEN = "momo123"
ACCESS_TOKEN = "EAAWy5YS0dxIBS4P1YelvLfQX3STZCPhCDXgSKiCoAZCTeSRZAREQ9VnL8nero6WAUNEzdeXAW8CmIPfZBuFjWwJ8PNj1Y8ZAsxZCEcVa4Pn38LKbzjGyUVO5s0YyGnP1FG96tpaNYQhjqDzh0fMHFFVngdFwP2ILI4bmYnTUYjq0bsqpYZAzDuxTeFGMKyTuYffhYQN687s6LKEWXtZCZCa45oa2SHY14qgWc46Xuz15NOP4QUBcI72jGCzHT1CBhBUIWbALyc2Fu03qklqW9oppx1akZD"
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
