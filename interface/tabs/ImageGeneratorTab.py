import asyncio
import base64
import io
import os
import threading
from datetime import datetime

import aiohttp
import requests
from PIL import Image
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Signal

from interface.urls import (
    LOCAL_URL
)


def ensure_dir(file_path):
    os.makedirs(file_path, exist_ok=True)


class CustomEvent(QtCore.QEvent):
    def __init__(self, image_data):
        super().__init__(QtCore.QEvent.Type.User)
        self.image_data = image_data


class ImageGeneratorTab(QtWidgets.QWidget):
    tab_selected = Signal()
    def __init__(self):
        super().__init__()
        self.status_label = None
        self.progress_bar = None
        self.scroll_area_widget = None
        self.text_input_error = None
        self.layout = None
        self.send_button = None
        self.count_input = None
        self.style_input = None
        self.negative_input = None
        self.text_input = None
        self.scroll_area = None
        self.scroll_layout = None
        self.current_ready_image = []
        self.current_settings = {}
        self.save_directory = None

        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        self.text_input = QtWidgets.QLineEdit(
            placeholderText="Введите запрос, например: нарисованный кистью и красками рисунок природы, море, горы, "
                            "сосны, спокойные цвета"
        )
        self.negative_input = QtWidgets.QLineEdit(placeholderText="Кусты, красные цветы, птицы")

        # Style dropdown with default selection
        self.style_input = QtWidgets.QComboBox()
        styles = self.get_styles()
        self.style_input.addItems([style["name"] for style in styles] if styles else [])
        self.style_input.setCurrentIndex(0)

        self.count_input = QtWidgets.QSpinBox()
        self.count_input.setRange(1, 10)
        self.count_input.setValue(1)

        # Send button with disabled state initially
        self.send_button = QtWidgets.QPushButton("Создать запрос на генерацию")
        self.send_button.setEnabled(True)
        self.send_button.clicked.connect(self.call_send_request)

        # Scroll area to contain generated images
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.scroll_area_widget = QtWidgets.QWidget()
        self.scroll_area_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.hide()
        self.status_label = QtWidgets.QLabel()
        ...

    def setup_layout(self):
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        save_button = QtWidgets.QPushButton("Сохранить")
        save_button.clicked.connect(self.save_images)
        save_dir_button = QtWidgets.QPushButton("Выбрать директорию для сохранения")
        save_dir_button.clicked.connect(self.select_save_directory)
        repeat_button = QtWidgets.QPushButton("Повторить с этим же запросом")
        repeat_button.clicked.connect(self.call_send_request)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(QtWidgets.QLabel("Описание картины:"))
        left_layout.addWidget(self.text_input)
        left_layout.addWidget(QtWidgets.QLabel("Чего не должно быть:"))
        left_layout.addWidget(self.negative_input)
        left_layout.addWidget(QtWidgets.QLabel("Стили:"))
        left_layout.addWidget(self.style_input)
        left_layout.addWidget(QtWidgets.QLabel("Количество картин:"))
        left_layout.addWidget(self.count_input)
        left_layout.addWidget(self.send_button)
        left_layout.addWidget(self.progress_bar)
        left_layout.addWidget(self.status_label)
        left_layout.addStretch()

        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(self.scroll_area)

        subprocess_layout = QtWidgets.QHBoxLayout()
        subprocess_layout.addWidget(save_button)
        subprocess_layout.addWidget(save_dir_button)
        subprocess_layout.addWidget(repeat_button)
        subprocess_layout.addStretch()
        right_layout.addLayout(subprocess_layout)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.tab_selected.emit()

    async def send_request(self):

        text = self.text_input.text().strip()
        if not text:
            self.progress_bar.hide()
            self.status_label.setText("Error: Описание не может быть пустым!")
            self.status_label.setStyleSheet("color: red;")
            return
        self.progress_bar.hide()
        self.status_label.setText(f"Задача отправлена, ожидайте примерно {20 * self.count_input.value()} секунд")
        self.status_label.setStyleSheet("color: white;")
        text = self.text_input.text()
        negative = self.negative_input.text()
        style = self.style_input.currentText()
        count_request = self.count_input.value()
        json = {
            "text": str(text),
            "style": str(style),
            "width": int(1024),
            "height": int(1024)
        }
        self.current_settings = {
            "text": str(text),
            "style": str(style),
            "width": int(1024),
            "height": int(1024)
        }
        if negative:
            json["negative"] = str(negative)

        if count_request:
            json["count_request"] = int(count_request)

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{LOCAL_URL}/api/v1/generate", json=json) as response:
                if response.status == 200:
                    self.progress_bar.hide()
                    self.status_label.setText("Изображения сгенерированы!")
                    self.status_label.setStyleSheet("color: green;")
                    response_json = await response.json()
                    for image_data in response_json:
                        event = CustomEvent(image_data)
                        QtCore.QCoreApplication.instance().postEvent(self, event)
                else:
                    self.progress_bar.hide()
                    self.status_label.setText(f"Error: Request failed with status code {response.status}")
                    self.status_label.setStyleSheet("color: red;")

    def call_send_request(self):
        def run_coroutine():
            asyncio.run(self.send_request())

        threading.Thread(target=run_coroutine).start()

    def update_gui(self, image_data):
        image = QtGui.QImage()
        image.loadFromData(base64.b64decode(image_data))
        self.current_ready_image.append(base64.b64decode(image_data))
        pixmap = QtGui.QPixmap.fromImage(image)
        label = QtWidgets.QLabel()
        label.setPixmap(pixmap.scaled(self.scroll_area.width(), self.scroll_area.height(),
                                      QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(label)
        self.progress_bar.hide()
        self.status_label.setText("Изображения сгенерированы!")
        self.status_label.setStyleSheet("color: green;")

    def handle_custom_event(self, event):
        image_data = event['image']
        self.update_gui(image_data)

    def event(self, event):
        t = event.type() == QtCore.QEvent.Type.User
        if t:
            self.handle_custom_event(event.image_data)
        return super().event(event)

    def mouseDoubleClickEvent(self, event):
        child = self.childAt(event.pos())
        if isinstance(child, QtWidgets.QLabel) and child.pixmap():
            pixmap = child.pixmap()
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Image Preview")
            dialog.resize(pixmap.width(), pixmap.height())
            label = QtWidgets.QLabel(dialog)
            label.setPixmap(pixmap)
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            dialog.exec()

    def text_input_focus_in(self, text):
        if text:
            self.text_input.setStyleSheet("")
            self.text_input_error.hide()

    @staticmethod
    def get_styles():
        response = requests.get(f"{LOCAL_URL}/api/v1/styles")
        if response.status_code == 200:
            return [style for style in response.json()]
        else:
            return []

    def save_images(self):
        if len(self.current_ready_image) > 0:
            for iteration, image in enumerate(self.current_ready_image):
                timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                filename = f"{self.current_settings['text'].replace(' ', '_')}_{timestamp}_{iteration}.jpg"
                if self.save_directory is None:
                    filepath = os.path.join(os.getcwd(), timestamp, str(iteration), filename)
                else:
                    filepath = os.path.join(self.save_directory, timestamp, str(iteration), filename)
                ensure_dir(os.path.dirname(filepath))

                i = Image.open(io.BytesIO(image))
                i.save(fp=filepath)

            sd = self.save_directory if self.save_directory is not None else os.path.join(os.getcwd(), timestamp,
                                                                                          str(iteration))
            self.progress_bar.hide()
            self.status_label.setText(f"Файлы успешно сохранены в {sd}")
        else:
            self.progress_bar.hide()
            self.status_label.setText(f"Чтобы что то сохранить - нужно что то создать")

    def select_save_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите директорию для сохранения",
                                                               os.path.expanduser("~"))
        if directory:
            self.save_directory = directory
