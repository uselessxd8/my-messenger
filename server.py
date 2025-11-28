from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Файл для сохранения сообщений
MESSAGES_FILE = "messages.json"


def load_messages():
    """Загружаем сообщения из файла"""
    try:
        if os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки сообщений: {e}")
    return []


def save_messages(messages):
    """Сохраняем сообщения в файл"""
    try:
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения сообщений: {e}")


# Загружаем сообщения при старте
messages = load_messages()


@app.route('/')
def home():
    return "✅ Сервер работает! Сообщения сохраняются."


@app.route('/send', methods=['POST'])
def send_message():
    try:
        data = request.json
        message = {
            'id': len(messages) + 1,
            'user': data.get('user', 'Аноним'),
            'text': data.get('text', ''),
            'time': datetime.datetime.now().strftime('%H:%M:%S'),
            'date': datetime.datetime.now().strftime('%Y-%m-%d')
        }
        messages.append(message)

        # Сохраняем в файл
        save_messages(messages)

        # Храним только последние 100 сообщений
        if len(messages) > 100:
            messages.pop(0)
            save_messages(messages)

        print(f"📨 {message['user']}: {message['text']}")
        return jsonify({'status': 'success'})

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return jsonify({'status': 'error'})


@app.route('/messages')
def get_messages():
    return jsonify(messages)


if __name__ == '__main__':
    print(f"🚀 Сервер запущен: http://localhost:5000")
    print(f"💾 Сообщения сохраняются в: {MESSAGES_FILE}")
    app.run(host='0.0.0.0', port=5000, debug=True)