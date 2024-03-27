import base64
import sys
import threading
import time

from PySide6 import QtCore, QtWidgets, QtGui
import requests
from server import app
from t2image.Text2Image import get_all_style

# Create an event to signal server startup
server_started_event = threading.Event()


def run_server():
    print("Starting server...")
    import uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
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


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        print("Server started\nInitializing GUI...")
        qss_file = open("assets/style/gitdark.qss", "r")
        with qss_file:
            st = qss_file.read()
            app.setStyleSheet(st)

        self.setWindowTitle("Text to Image API")
        self.setFixedSize(1280, 800)

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
        self.send_button.setEnabled(True)  # Disable until server is ready
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
        negative = self.negative_input.text() if self.negative_input.text() != '' else "nullptr"
        style = self.style_input.currentText()
        count_request = self.count_input.value()
        print(text, negative, style, int(count_request), 1, str('1024'), str('1024'))
        response = requests.post(
            "http://0.0.0.0:8000/api/v1/generate",
            data={
                "text": text,
                "negative": negative,
                "style": style,
                "count_request": count_request,
                "width": 1024,
                "height": 1024
            },
        )

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
