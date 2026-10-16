from flask import Flask, request
import requests

app = Flask(__name__)
VERIFY_TOKEN = "momo_verify_123"
ACCESS_TOKEN = "EAAWy5YS0dxIBSxNS6rdZBauPVI5JbbmfWm9w0GWmsZBnB9BmyZBUSKTO2ji7Abz3rA91AQJod8YRZBgoSxaZB1Kghp2hWFG5vS2u6DmS3UZAXNZByKGawVZACmqftiHpq8sJESCwPZBpCyB0rYaxwXURlqPZCL2Sa6c1S75n2SuTbH8Sv50QCOeS5kUXjAHh6zKE5VRaZBm9pM0JaiT9eZA3ZAkVsBP9Rm0tWKskPZB7AFoncxWMUKUrrvZAqpKaZCsLlqtL4wPHrRW2UUGexVY7dD9E2ZCYx7wZDZD"
PHONE_NUMBER_ID = "1129454846925725"

@app.route('/api/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge'), 200
    return 'Fail', 403

@app.route('/api/webhook', methods=['POST'])
def incoming():
    data = request.get_json()
    try:
        v = data['entry'][0]['changes'][0]['value']
        if 'messages' in v:
            msg = v['messages'][0]
            num = msg['from']
            txt = msg.get('text', {}).get('body','')
            url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
            requests.post(url, headers={"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type":"application/json"}, json={"messaging_product":"whatsapp","to":num,"type":"text","text":{"body":f"وصلتني رسالتك: {txt} - بوت مومو شغال ✅"}})
    except Exception as e:
        print(e)
    return "OK", 200
