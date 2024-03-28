# MainWindow.py - Main window of the application

from PySide6 import QtWidgets

from interface.ChatTab import ChatTab
from interface.ImageGeneratorTab import ImageGeneratorTab

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        ...

    def initialize_ui(self):
        print("Server started\nInitializing GUI...")
        qss_file = open("assets/style/neon.qss", "r")
        with qss_file:
            st = qss_file.read()
            self.setStyleSheet(st)

        self.setWindowTitle("Kandinsky Image Generator API/UI")
        self.setFixedSize(1280, 800)

        # Create tab widget
        tab_widget = QtWidgets.QTabWidget()
        tab_widget.setFixedWidth(1200)

        # Create tabs
        image_generator_tab = ImageGeneratorTab()
        chat_tab = ChatTab()

        # Add tabs to tab widget
        tab_widget.addTab(image_generator_tab, "Image Generator")
        tab_widget.addTab(chat_tab, "Chat")

        # Create 5 empty tabs
        for i in range(3, 8):
            tab = QtWidgets.QWidget()
            tab_widget.addTab(tab, f"Tab {i}")
        # Set central widget to the tab widget
        self.setCentralWidget(tab_widget)

        # Copyright information (optional)
        copyright_label = QtWidgets.QLabel("Copyright © 2023 massonskyi")
        status_bar = self.statusBar()
        status_bar.addPermanentWidget(copyright_label)
        print("Application started")


