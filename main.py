import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Qudra Bot LIVE! Created by Abdulmalik - WhatsApp Ready!"

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.mode') == 'subscribe':
            return request.args.get('hub.challenge')
        return "Qudra Webhook Live"
    else:
        data = request.get_json()
        print(data)
        return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
