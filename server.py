from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

messages = []

@app.route('/')
def home():
    return "✅ Сервер работает!"

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    message = {
        'user': data.get('user', 'Аноним'),
        'text': data.get('text', ''),
        'time': datetime.datetime.now().strftime('%H:%M:%S')
    }
    messages.append(message)
    print(f"📨 {message['user']}: {message['text']}")
    return jsonify({'status': 'success'})

@app.route('/messages')
def get_messages():
    return jsonify(messages)

if __name__ == '__main__':
    print("🚀 Сервер запущен: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)