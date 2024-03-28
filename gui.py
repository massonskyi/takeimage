import base64
import sys
import threading
import time

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtGui import QLinearGradient, QColor
from PySide6.QtWidgets import QGraphicsOpacityEffect

import requests
from server import app

# Create an event to signal server startup
server_started_event = threading.Event()


def run_server():
    print("Starting server...")
    import uvicorn
    config = uvicorn.Config(app.app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)

    server_started_event.set()
    server.run()


def check_server_status():
    if server_started_event.is_set():
        print("Server is ready!")
        return True
    else:
        # Handle server not yet ready (e.g., display a waiting message)
        print("Server not yet ready...")
        return False


class GradientBackground(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._gradientOffset = 0
        self.gradient = QtGui.QLinearGradient(0, 0, 0, self.height())
        self.gradient.setSpread(QtGui.QGradient.Spread.ReflectSpread)
        self.gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        self.gradient.setColorAt(0.0, QtGui.QColor("#f3e6ff"))  # Верхний цвет
        self.gradient.setColorAt(1.0, QtGui.QColor("#a6c1ee"))  # Нижний цвет

        self.animation = QtCore.QPropertyAnimation(self, b"gradientOffset")
        self.animation.setStartValue(0)
        self.animation.setEndValue(self.height())
        self.animation.setDuration(5000)  # Время анимации в миллисекундах
        self.animation.setLoopCount(-1)  # Бесконечный цикл

        self.animation.finished.connect(self.animationFinished)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.gradient)

    def getGradientOffset(self):
        return self._gradientOffset

    def setGradientOffset(self, value):
        self._gradientOffset = value
        self.gradient.setStart(0, value)
        self.gradient.setFinalStop(0, value + self.height())
        self.update()

    gradientOffset = QtCore.Property(int, getGradientOffset, setGradientOffset)

    def animationFinished(self):
        # При завершении анимации начинаем ее заново
        self.animation.start()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        print("Server started\nInitializing GUI...")
        qss_file = open("assets/style/neon.qss", "r")
        with qss_file:
            st = qss_file.read()
            app.setStyleSheet(st)

        self.setWindowTitle("Text to Image API")
        self.setFixedSize(1280, 800)
        self.gradientBackground = GradientBackground()
        # Text input fields
        self.text_input = QtWidgets.QLineEdit(placeholderText="Enter text")
        self.negative_input = QtWidgets.QLineEdit(placeholderText="Enter negative (optional)")

        # Style dropdown with default selection
        self.style_input = QtWidgets.QComboBox()
        styles = self.get_styles()  # Fetch styles from server upon initialization (optional)
        self.style_input.addItems([style["name"] for style in styles] if styles else [])
        self.style_input.setCurrentIndex(0)  # Select the first style by default (optional)

        self.count_input = QtWidgets.QSpinBox()
        self.count_input.setRange(1, 10)
        self.count_input.setValue(1)

        # Send button with disabled state initially
        self.send_button = QtWidgets.QPushButton("Generate Images")
        self.send_button.setEnabled(True)
        self.send_button.clicked.connect(self.send_request)

        self.layout = QtWidgets.QVBoxLayout()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(QtWidgets.QWidget())
        self.scroll_area.widget().setLayout(self.layout)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(QtWidgets.QLabel("Text:"))
        main_layout.addWidget(self.text_input)
        main_layout.addWidget(QtWidgets.QLabel("Negative:"))
        main_layout.addWidget(self.negative_input)
        main_layout.addWidget(QtWidgets.QLabel("Style:"))
        main_layout.addWidget(self.style_input)
        main_layout.addWidget(QtWidgets.QLabel("Count:"))
        main_layout.addWidget(self.count_input)
        main_layout.addWidget(self.send_button)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.gradientBackground)
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Copyright information (optional)
        copyright_label = QtWidgets.QLabel("Copyright © 2023 massonskyi")
        status_bar = self.statusBar()
        status_bar.addPermanentWidget(copyright_label)

        print("Application started")

    def send_request(self):
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

        if negative:
            json["negative"] = str(negative)

        if count_request:
            json["count_request"] = int(count_request)

        response = requests.post("http://0.0.0.0:8000/api/v1/generate", json=json)

        if response.status_code == 200:
            for image_data in response.json():
                image = QtGui.QImage()
                image.loadFromData(base64.b64decode(image_data["image"]))
                image_label = QtWidgets.QLabel()
                image_label.setPixmap(QtGui.QPixmap.fromImage(image))
                image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.layout.addWidget(image_label)
        else:
            QtWidgets.QMessageBox.critical(self, "Error", f"Request failed with status code {response.status_code}")

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
            dialog.exec_()

    @staticmethod
    def get_styles():
        response = requests.get("http://0.0.0.0:8000/api/v1/styles")
        if response.status_code == 200:
            return [style for style in response.json()]
        else:
            return []


if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()

    while not check_server_status():
        time.sleep(2)

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
