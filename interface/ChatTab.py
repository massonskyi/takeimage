# ChatTab.py
import asyncio

import aiohttp
from PySide6 import QtWidgets, QtCore

from interface.subwindow.SettingsChatWindow import SettingsWindow


class ChatTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Chat history
        self.chat_history = QtWidgets.QTextEdit()
        self.chat_history.setReadOnly(True)

        # User input
        self.user_input = QtWidgets.QLineEdit()
        self.user_input.returnPressed.connect(self.on_send_button_clicked)
        self.user_input.installEventFilter(self)
        # Send button
        self.send_button = QtWidgets.QPushButton("Send")
        self.send_button.clicked.connect(self.on_send_button_clicked)

        # Layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.chat_history)
        input_layout = QtWidgets.QHBoxLayout()
        input_layout.addWidget(self.user_input)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)

        # Settings button
        self.settings_button = QtWidgets.QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)

        # Add settings button to the layout
        input_layout.addWidget(self.settings_button)

        # Other parameters
        self.temperature = 0.7
        self.top_p = 0.1
        self.n = 1
        self.max_tokens = 525
        self.repetition_penalty = 1.0

        # Add welcome message
        self.add_message("Welcome to the chat!", "program")
        self._loop = asyncio.get_event_loop()

    def eventFilter(self, source, event):
        if source == self.user_input and event.type() == QtCore.QEvent.Type.KeyPress:
            if event.key() == QtCore.Qt.Key.Key_Enter:
                self.on_send_button_clicked()
                return True
        return super().eventFilter(source, event)

    def open_settings(self):
        settings_window = SettingsWindow(self)
        settings_window.exec()

    async def send_message(self):
        user_message = self.user_input.text()
        if user_message:
            self.add_message(user_message, "user")
            json = {
                'query': user_message,
                'temperature': float(self.temperature),
                'top_p': float(self.top_p),
                'n': int(self.n),
                'stream': False,
                'max_tokens': int(self.max_tokens),
                'repetition_penalty': self.repetition_penalty
            }
            print(json)  # Print JSON data for debugging
            async with aiohttp.ClientSession() as session:
                async with session.post('http://0.0.0.0:8000/api/v1/quest', json=json) as response:
                    if response.status == 200:
                        data = await response.json()
                        response = data[0]['answer']
                        self.add_message(response, "program")
                    else:
                        self.add_message(f"Error: {response.status}", "program")

            self.user_input.clear()

    def on_send_button_clicked(self):
        task = asyncio.ensure_future(self.send_message())

        def done_callback(task):
            self._loop.stop()

        task.add_done_callback(done_callback)  # Stop the loop when the task is done
        self._loop.run_forever()  # Run the loop until the task is done

    def add_message(self, message, sender):
        sender_label = "You" if sender == "user" else "Program"
        formatted_message = f"<b>{sender_label}:</b> {message}"
        self.chat_history.append(formatted_message)
