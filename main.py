from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import requests
import threading


class PCMessengerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Заголовок
        title = Label(text='💬 Наш Мессенджер', font_size='20sp')
        layout.add_widget(title)

        # Область сообщений
        self.chat_scroll = ScrollView()
        self.chat_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_scroll.add_widget(self.chat_layout)
        layout.add_widget(self.chat_scroll)

        # Поле ввода
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        self.message_input = TextInput(hint_text='Введите сообщение...')
        self.send_button = Button(text='Отправить')
        self.send_button.bind(on_press=self.send_message)

        input_layout.add_widget(self.message_input)
        input_layout.add_widget(self.send_button)
        layout.add_widget(input_layout)

        # Автообновление каждые 2 секунды
        Clock.schedule_interval(self.load_messages, 2)

        return layout

    def send_message(self, instance):
        message = self.message_input.text
        if message:
            threading.Thread(target=self.send_to_server, args=(message,)).start()
            self.message_input.text = ''

    def send_to_server(self, message):
        try:
            requests.post('http://localhost:5000/send',
                          json={'user': 'Ты', 'text': message})
            self.load_messages()
        except Exception as e:
            print(f"Ошибка: {e}")

    def load_messages(self, dt=None):
        threading.Thread(target=self.load_from_server).start()

    def load_from_server(self):
        try:
            response = requests.get('http://localhost:5000/messages')
            messages = response.json()
            self.update_chat(messages)
        except Exception as e:
            print(f"Ошибка загрузки: {e}")

    def update_chat(self, messages):
        # Очищаем чат в основном потоке Kivy
        def update_in_main_thread():
            self.chat_layout.clear_widgets()
            for msg in messages:
                label = Label(
                    text=f"{msg['user']}: {msg['text']}",
                    size_hint_y=None,
                    height=40,
                    text_size=(None, None)
                )
                label.bind(texture_size=label.setter('size'))
                self.chat_layout.add_widget(label)

        # Запускаем обновление в основном потоке
        Clock.schedule_once(lambda dt: update_in_main_thread())

if __name__ == '__main__':
    PCMessengerApp().run()