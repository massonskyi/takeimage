# -*- coding: utf-8 -*-
# !/usr/bin/env python
# main.py
import sys
import threading
import time

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication
import asyncio
from interface.MainWindow import MainWindow
from interface.server import run_server, server_started_event


def check_server_status():
    if server_started_event.is_set():
        print("Server is ready!")
        return True
    else:
        # Handle server not yet ready (e.g., display a waiting message)
        print("Server not yet ready...")
        return False


class AsyncQApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    def exec_(self):
        self._loop.run_forever()
        super().exec_()


if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()

    while not check_server_status():
        time.sleep(2)

    app = AsyncQApplication([])

    window = MainWindow()
    window.initialize_ui()
    window.show()

    sys.exit(app.exec())
