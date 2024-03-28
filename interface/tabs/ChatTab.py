import asyncio
import json

import aiohttp
from PySide6 import QtCore, QtWidgets
from interface.urls import LOCAL_URL
from interface.subwindow.SettingsChatWindow import SettingsWindow


def extract_color(style_sheet):
    if style_sheet:
        parts = style_sheet.split(": ")
        if len(parts) == 2:
            return parts[1][:-1]
    return None


class ChatTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._bot_color = None
        self._user_color = None
        self._font_size = 14
        self._font_weight = "normal"
        self._border_width = 2
        self._border_color = "#FFFFFF"
        self._background_color = "#282a36"

        # Chat history
        self.chat_history = QtWidgets.QTextEdit()
        self.chat_history.setReadOnly(True)
        self.apply_textedit_styles()  # Применить стили к истории чата

        # User input
        self.user_input = QtWidgets.QLineEdit()
        self.user_input.returnPressed.connect(self.on_send_button_clicked)
        self.user_input.installEventFilter(self)
        self.apply_lineedit_styles()  # Применить стили к полю ввода пользователя

        # Send button
        self.send_button = QtWidgets.QPushButton("Спросить")
        self.apply_send_button_styles()  # Применить стили к кнопке отправки
        self.send_button.clicked.connect(self.on_send_button_clicked)

        # Layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.chat_history)
        input_layout = QtWidgets.QHBoxLayout()
        input_layout.addWidget(self.user_input)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)

        self.settings_button = QtWidgets.QPushButton("Настройки")
        self.apply_settings_button_styles()  # Применить стили к кнопке настроек
        self.settings_button.clicked.connect(self.open_settings)
        input_layout.addWidget(self.settings_button)

        # Other parameters
        self.temperature = 0.7
        self.top_p = 0.1
        self.n = 1
        self.max_tokens = 525
        self.repetition_penalty = 1.0

        # Add welcome message
        self.add_message("Здравствуйте!", "program")
        self._loop = asyncio.get_event_loop()
        self.load_default_styles()  # Загрузить стили по умолчанию
        self.load_user_settings()  # Загрузить настройки пользователя

    def load_default_styles(self):
        qss_file = open("assets/style/darksynthic84.qss", "r")
        with qss_file:
            st = qss_file.read()
            self.setStyleSheet(st)

    def load_user_settings(self):
        try:
            with open("assets/settings.json", "r") as file:
                settings = json.load(file)
                # Установка сохраненных параметров
                self._user_color = extract_color(settings.get("user_color", "#FFFFFF"))
                self._bot_color = extract_color(settings.get("bot_color", "#00FF00"))
                self._background_color = extract_color(settings.get("background_color", "#282a36"))
                self._border_color = extract_color(settings.get("border_color", "#FFFFFF"))
                # Применяем значения к виджетам
                self.apply_styles()
        except FileNotFoundError:
            # Если файл не найден, используем значения по умолчанию
            self._user_color = "#FFFFFF"
            self._bot_color = "#00FF00"
            self._background_color = "#282a36"
            self._border_color = "#FFFFFF"
            # Применяем значения по умолчанию к виджетам
            self.apply_styles()

    def apply_textedit_styles(self):
        self.chat_history.setStyleSheet("""
                    QTextEdit {
                        background-color: %s;
                        color: #f8f8f2;
                        border: %dpx solid %s;
                        padding: 10px;
                    }
                    QTextEdit hr {
                        border: none;
                        border-top: 1px solid #44475a;
                        margin: 5px 0;
                    }
                """ % (self._background_color, self._border_width, self._border_color))

    def apply_lineedit_styles(self):
        self.user_input.setStyleSheet("""
                    QLineEdit {
                        background-color: #44475a;
                        color: #f8f8f2;
                        border-radius: 5px;
                        padding: 5px;
                    }
                """)

    def apply_send_button_styles(self):
        self.send_button.setStyleSheet("""
                    QPushButton {
                        background-color: #585b70;
                        color: #f8f8f2;
                        border-radius: 5px;
                        padding: 5px 10px;
                    }
                    QPushButton:hover {
                        background-color: #6c6f85;
                    }
                    QPushButton:pressed {
                        background-color: #44475a;
                    }
                """)

    def apply_settings_button_styles(self):
        self.settings_button.setStyleSheet("""
                    QPushButton {
                        background-color: #585b70;
                        color: #f8f8f2;
                        border-radius: 5px;
                        padding: 5px 10px;
                    }
                    QPushButton:hover {
                        background-color: #6c6f85;
                    }
                    QPushButton:pressed {
                        background-color: #44475a;
                    }
                """)

    def eventFilter(self, source, event):
        if source == self.user_input and event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Enter:
                self.send_message()  # Вызов метода send_message вместо on_send_button_clicked
                return True
        return super().eventFilter(source, event)

    def open_settings(self):
        settings_window = SettingsWindow(self)
        settings_window.exec()

    async def send_message(self):
        user_message = self.user_input.text()
        if user_message:
            json_data = {
                'query': user_message,
                'temperature': float(self.temperature),
                'top_p': float(self.top_p),
                'n': int(self.n),
                'stream': False,
                'max_tokens': int(self.max_tokens),
                'repetition_penalty': self.repetition_penalty
            }
            print(json_data)  # Print JSON data for debugging
            async with aiohttp.ClientSession() as session:
                async with session.post(f'{LOCAL_URL}/api/v1/quest', json=json_data) as response:
                    if response.status == 200:
                        data = await response.json()
                        response = data[0]['answer']
                        self.add_message(response, "program")
                    else:
                        self.add_message(f"Error: {response.status}", "program")
            self.user_input.clear()

    def on_send_button_clicked(self):
        self.add_message(self.user_input.text(), "user")
        task = asyncio.ensure_future(self.send_message())

        def done_callback(task):
            self._loop.stop()

        task.add_done_callback(done_callback)  # Stop the loop when the task is done
        self._loop.run_forever()  # Run the loop until the task is done

    def set_temperature(self, temperature: float):
        self.temperature = temperature

    def set_top_p(self, top_p: float):
        self.top_p = top_p

    def set_repetition_penalty(self, repetition_penalty):
        self.repetition_penalty = repetition_penalty

    def set_max_tokens(self, max_tokens):
        self.max_tokens = max_tokens

    def set_n(self, n):
        self.n = n

    def apply_styles(self):
        style_sheet = f"""
            QTextEdit {{
                background-color: {self._background_color};
                color: {self._user_color};
                border: {self._border_width}px solid {self._border_color};
                padding: 10px;
                font-size: {self._font_size}pt;
                font-weight: {self._font_weight};
            }}
        """
        self.chat_history.setStyleSheet(style_sheet)

    def set_font_size(self, font_size):
        self._font_size = font_size
        self.apply_styles()

    def set_font_weight(self, font_weight):
        self._font_weight = font_weight
        self.apply_styles()

    def set_user_color(self, user_color):
        self._user_color = user_color
        self.apply_styles()

    def set_bot_color(self, bot_color):
        self._bot_color = bot_color
        self.apply_styles()

    def set_background_color(self, background_color):
        self._background_color = background_color
        self.apply_styles()

    def set_border_color(self, border_color):
        self._border_color = border_color
        self.apply_styles()

    def add_message(self, message, sender):
        sender_label = "Вы" if sender == "user" else "Бот"
        color = self._user_color if sender == "user" else self._bot_color
        formatted_message = f"<span style='font-size: 14pt; font-weight: bold; color: {color};'>{sender_label}: {message}</span>"
        self.chat_history.append(formatted_message)
