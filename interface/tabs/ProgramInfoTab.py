from PySide6.QtCore import QThread, Signal, QDateTime, QTimer, Qt
from PySide6 import QtWidgets
from PySide6.QtWidgets import QScrollArea

license_text = """
Лицензионное соглашение

1. Предмет лицензии

Программа, включая все связанные с ней файлы и документацию,\n
предоставляется на условиях данного лицензионного соглашения.
\nПод "программой" понимается компьютерная программа, разработанная MASSONSKYI.

2. Права на интеллектуальную собственность

MASSONSKYI оставляет за собой все права на интеллектуальную собственность в отношении программы,\n
включая, но не ограничиваясь, авторскими правами и патентами.

3. Лицензионные права

Пользователь получает неисключительное право на использование\n
программы в соответствии с условиями данного соглашения.

4. Ограничения использования

Пользователь не имеет права:
   - копировать, модифицировать, распространять или продавать программу или ее части;
   - переводить, адаптировать, обратно-компилировать или разбирать программу;
   - удалять или изменять любые знаки авторского права, \n
   торговые марки или другие уведомления об интеллектуальной\nсобственности.
   
5. Отказ от гарантий

Программа предоставляется "как есть", без каких-либо гарантий,\n
явных или подразумеваемых. MASSONSKYI не несет ответственности \n
за любые убытки, прямые или косвенные, возникшие в результате\n
использования или невозможности использования программы.
6. Ответственность

MASSONSKYI не несет ответственности за любые случайные,\n
специальные, непрямые или косвенные убытки\n
или ущерб, возникшие в результате использования программы или связанных с ней услуг.

7. Изменения в лицензии

MASSONSKYI оставляет за собой право изменять условия данного лицензионного соглашения в любое время.

8. Принятие условий

Установка или использование программы означает согласие пользователя с условиями данного лицензионного соглашения.
"""


class Worker(QThread):
    update_signal = Signal(str)
    timer_timeout = Signal()

    def __init__(self):
        super().__init__()

    def run(self):
        timer = QTimer()
        timer.timeout.connect(self.timer_timeout)
        timer.start(1000)
        self.timer_timeout.connect(self.update_time)
        self.exec_()

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString(Qt.DateFormat.TextDate)
        self.update_signal.emit(current_time)


class ProgramInfoTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.current_time_label = None
        self.initialize_ui()
        self.worker = Worker()
        self.worker.update_signal.connect(self.update_time)
        self.worker.start()
        # Подключаем событие закрытия окна
        self.destroyed.connect(self.stop_worker)

    def initialize_ui(self):
        layout = QtWidgets.QGridLayout()

        # Лицензионное соглашение
        license_label = QtWidgets.QLabel(license_text)
        # Создаем область прокрутки и устанавливаем метку с лицензионным соглашением внутри нее
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(license_label)

        layout.addWidget(scroll_area, 0, 0)
        # Автор программы
        author_label = QtWidgets.QLabel("<MASSONSKYI> <2024-03-28>")
        layout.addWidget(author_label, 0, 2)

        # Полезные ссылки
        links_label = QtWidgets.QLabel("Полезные ссылки")
        layout.addWidget(links_label, 2, 0)

        # Текущее время
        self.current_time_label = QtWidgets.QLabel()
        layout.addWidget(self.current_time_label, 2, 2)

        self.setLayout(layout)

    def update_time(self, time_str):
        self.current_time_label.setText(time_str)

    def stop_worker(self):
        self.worker.quit()  # Завершаем работу потока Worker
