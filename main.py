# -*- coding: utf-8 -*-
# !/usr/bin/env python
# main.py

import os
import sys
import threading
import time

from PySide6.QtWidgets import QApplication
import asyncio
from interface.MainWindow import MainWindow
from interface.server import run_server, server_started_event


def check_server_status():
    if server_started_event.is_set():
        print("Server is ready!")
        return True
    else:
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


def check_and_create_critical_items(critical_items) -> bool:
    missing_items = []
    for item in critical_items:
        if os.path.exists(item):
            print(f"Файл: {item} найден.") if os.path.isfile(item) else print(f"Директория: {item} найден.")
        else:
            print(f"Файл: {item} отсутствует и будет создан.") if os.path.isfile(item) \
                else print(f"Директория: {item} отсутствует и будет создан.")
            try:
                if '.' in item:
                    with open(item, 'w') as file:
                        pass
                else:
                    os.makedirs(item)
                print(f"{item} успешно создан.")
            except Exception as e:
                print(f"Ошибка при создании {item}: {e}")
                missing_items.append(item)
    if missing_items:
        print("Не удалось создать следующие элементы:", missing_items)
        return False
    else:
        print("Все критически важные элементы найдены или созданы.")
        return True


critical_items = ["config.env", "assets", "interface", "modules", "server", "config.py"]

if __name__ == "__main__":
    if not check_and_create_critical_items(critical_items):
        exit(-1)

    threading.Thread(target=run_server, daemon=True).start()

    """
    time.sleep(2)
    while not check_server_status():
        time.sleep(2)
    """

    app = AsyncQApplication([])

    window = MainWindow()
    window.initialize_ui()
    window.show()

    sys.exit(app.exec())
