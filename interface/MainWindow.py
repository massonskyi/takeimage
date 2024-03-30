# MainWindow.py - Main window of the application
import os

from PySide6 import QtWidgets

from config import read_env
from interface.subwindow.TokenMissingWidget import TokenMissingWidget
from interface.tabs.ChatTab import ChatTab
from interface.tabs.ImageGeneratorTab import ImageGeneratorTab
from interface.tabs.ProgramInfoTab import ProgramInfoTab


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

        self.setWindowTitle("Client")
        self.setFixedSize(1280, 800)

        # Create tab widget
        tab_widget = QtWidgets.QTabWidget()
        tab_widget.setFixedWidth(1200)

        # Create tabs
        image_generator_tab = ImageGeneratorTab()
        image_generator_tab.tab_selected.connect(self.check_config_file)
        chat_tab = ChatTab()
        program_info_tab = ProgramInfoTab()  # New program info tab
        chat_tab = ChatTab()
        program_info_tab = ProgramInfoTab()  # New program info tab

        # Add tabs to tab widget
        tab_widget.addTab(image_generator_tab, "Image Generator")
        tab_widget.addTab(chat_tab, "Chat")
        # Create 4 empty tabs
        for i in range(3, 6):
            tab = QtWidgets.QWidget()
            tab_widget.addTab(tab, f"Tab {i}")
        tab_widget.addTab(program_info_tab, "Информация о программе")  # Add program info tab

        # Set central widget to the tab widget
        self.setCentralWidget(tab_widget)

        # Copyright information (optional)
        copyright_label = QtWidgets.QLabel("Copyright © 2023 massonskyi")
        status_bar = self.statusBar()
        status_bar.addPermanentWidget(copyright_label)
        print("Application started")

    def check_config_file(self):
        env_vars = read_env()
        env_vars_ch = read_env("gchcfg.env")
        if "KANDINSKY_TOKEN" not in env_vars or "KANDINSKY_SECRET_KEY" not in env_vars:
            self.show_token_missing_widget("KANDINSKY_TOKEN",
                                           "https://fusionbrain.ai/docs/doc/poshagovaya-instrukciya-po-upravleniu-api-kluchami/",
                                           "kan")
        if "RqUID" not in env_vars_ch or "authorization_data" not in env_vars_ch or "payload_data" not in env_vars_ch:
            self.show_token_missing_widget("gigachat token",
                                           "https://developers.sber.ru/docs/ru/gigachat/individuals-quickstart?tool=python",
                                           "gchat")

    #
    def show_token_missing_widget(self, token_missing, info, token_index):
        token_missing_widget = TokenMissingWidget(token_missing, info, token_index)
        token_missing_widget.finished.connect(self.on_token_missing_widget_finished)
        token_missing_widget.tokens_saved.connect(self.check_config_file)
        token_missing_widget.exec()

    def on_token_missing_widget_finished(self, result):
        if result == QtWidgets.QDialog.Accepted:
            env_vars = read_env()
            env_vars_ch = read_env("gchcfg.env")
            if "KANDINSKY_TOKEN" not in env_vars or "KANDINSKY_SECRET_KEY" not in env_vars:
                QtWidgets.QMessageBox.information(self, "Information", "Without tokens, the application cannot work.")
                self.close()
            if "RqUID" not in env_vars_ch or "authorization_data" not in env_vars_ch or "payload_data" not in env_vars_ch:
                QtWidgets.QMessageBox.information(self, "Information", "Without tokens, the application cannot work.")
                self.close()

        if result == QtWidgets.QDialog.Rejected:
            QtWidgets.QMessageBox.information(self, "Information",
                                              "Without tokens, the application cannot work. The application will now close.")
            self.close()
