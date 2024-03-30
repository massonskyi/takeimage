import re
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Signal

from config import write_env


class TokenMissingWidget(QtWidgets.QDialog):
    tokens_saved = Signal()

    def __init__(self, token_missing, info, token_index):
        super().__init__()
        self.setWindowTitle("Missing Tokens")
        self.setFixedSize(600, 300)
        self.token_index = token_index
        layout = QtWidgets.QVBoxLayout()

        info_with_link = f'<a href="{info}">Click here to get the token</a>'
        message_text = f"{token_missing} не найден.<br><br>" \
                       f"Пожалуйста, следуйте инструкции по его получению:<br><br>" \
                       f"{info_with_link}"
        message_browser = QtWidgets.QTextBrowser()
        message_browser.setOpenExternalLinks(True)
        message_browser.setHtml(message_text)
        layout.addWidget(message_browser)

        if self.token_index == 'kan':
            token_label = QtWidgets.QLabel("Введите токен:")
            self.token_input = QtWidgets.QLineEdit()
            layout.addWidget(token_label)
            layout.addWidget(self.token_input)

            secret_label = QtWidgets.QLabel("Введите секрет:")
            self.secret_input = QtWidgets.QLineEdit()
            layout.addWidget(secret_label)
            layout.addWidget(self.secret_input)
        elif self.token_index == 'gchat':
            scope_label = QtWidgets.QLabel("Введите scope:")
            self.scope_input = QtWidgets.QLineEdit()
            layout.addWidget(scope_label)
            layout.addWidget(self.scope_input)

            secret_label = QtWidgets.QLabel("Введите секрет:")
            self.secret_input = QtWidgets.QLineEdit()
            layout.addWidget(secret_label)
            layout.addWidget(self.secret_input)

            auth_data_label = QtWidgets.QLabel("Введите авторизационный токен:")
            self.auth_data_input = QtWidgets.QLineEdit()
            layout.addWidget(auth_data_label)
            layout.addWidget(self.auth_data_input)
        else:
            token_label = QtWidgets.QLabel("Вы попали сюда случайно :)")
            layout.addWidget(token_label)

        ok_button = QtWidgets.QPushButton("OK")
        ok_button.clicked.connect(self.save_tokens)
        layout.addWidget(ok_button, alignment=QtCore.Qt.AlignHCenter)

        self.setLayout(layout)

        self.token_regex = re.compile(r'^[0-9A-Fa-f]+$')

    def save_tokens(self):
        if self.token_index is None:
            self.accept()
        if self.token_index == 'kan':
            token = self.token_input.text().strip()
            secret = self.secret_input.text().strip()
            if not self.token_regex.match(token):
                QtWidgets.QMessageBox.warning(self, "Внимание!", "Неверный формат токена. "
                                                                 "Пожалуйста, проверьте правильность ввода.")
                return

            if not self.token_regex.match(secret):
                QtWidgets.QMessageBox.warning(self, "Внимание!", "Неверный формат секрета. "
                                                                 "Пожалуйста, проверьте правильность ввода.")
                return

            env_vars = {
                'KANDINSKY_TOKEN': token,
                'KANDINSKY_SECRET_KEY': secret
            }
            write_env(env_vars)
            self.accept()
            self.tokens_saved.emit()
        if self.token_index == 'gchat':
            rq_uid = self.secret_input.text().strip()
            payload = self.scope_input.text().strip()
            auth_token = self.auth_data_input.text().strip()

            if not rq_uid:
                QtWidgets.QMessageBox.warning(self, "Warning", "Invalid RqUsID format. Please check your input.")
                return

            if not auth_token:
                QtWidgets.QMessageBox.warning(self, "Warning",
                                              "Invalid authosrization_data format. Please check your input.")
                return

            if not payload:
                QtWidgets.QMessageBox.warning(self, "Warning", "Invalid paylosad_data format. Please check your input.")
                return

            env_vars = {
                'RqUID': rq_uid,
                'authorization_data': auth_token,
                'payload_data': payload
            }
            write_env(env_vars, "gchcfg.env")
            self.accept()
            self.tokens_saved.emit()
