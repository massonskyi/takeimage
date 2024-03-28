import json

from PySide6 import QtWidgets


def extract_color(style_sheet):
    if style_sheet:
        parts = style_sheet.split(": ")
        if len(parts) == 2:
            return parts[1][:-1]
    return None


def set_button_color(button, color):
    if color:
        button.setStyleSheet(f"background-color: {color};")


class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, chat_tab):
        super().__init__()
        self.chat_tab = chat_tab
        self.initialize_ui()

    def initialize_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Create input fields for parameters
        self.temperature_field = QtWidgets.QDoubleSpinBox()
        self.temperature_field.setValue(self.chat_tab.temperature)

        self.top_p_field = QtWidgets.QDoubleSpinBox()
        self.top_p_field.setValue(self.chat_tab.top_p)

        self.n_field = QtWidgets.QSpinBox()
        self.n_field.setValue(self.chat_tab.n)

        self.max_tokens_field = QtWidgets.QSpinBox()
        self.max_tokens_field.setValue(self.chat_tab.max_tokens)

        self.repetition_penalty_field = QtWidgets.QDoubleSpinBox()
        self.repetition_penalty_field.setValue(self.chat_tab.repetition_penalty)

        # Create font size combo box
        self.font_size_combo = QtWidgets.QComboBox()
        self.font_size_combo.addItems([str(size) for size in range(8, 31)])
        self.font_size_combo.setCurrentText("16")

        # Create font weight combo box
        self.font_weight_combo = QtWidgets.QComboBox()
        self.font_weight_combo.addItems(["Normal", "Bold"])
        self.font_weight_combo.setCurrentIndex(1)

        # Create message color labels and buttons
        self.user_color_label = QtWidgets.QLabel("User message color:")
        self.user_color_button = QtWidgets.QPushButton()
        self.user_color_button.clicked.connect(self.set_user_color)

        self.bot_color_label = QtWidgets.QLabel("Bot message color:")
        self.bot_color_button = QtWidgets.QPushButton()
        self.bot_color_button.clicked.connect(self.set_bot_color)

        # Create background color fields
        self.background_color_label = QtWidgets.QLabel("Background color:")
        self.background_color_button = QtWidgets.QPushButton()
        self.background_color_button.clicked.connect(self.set_background_color)

        # Create border color fields
        self.border_color_label = QtWidgets.QLabel("Border color:")
        self.border_color_button = QtWidgets.QPushButton()
        self.border_color_button.clicked.connect(self.set_border_color)

        # Create OK and Cancel buttons
        self.ok_button = QtWidgets.QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        # Add widgets to layout
        layout.addWidget(self.temperature_field)
        layout.addWidget(self.top_p_field)
        layout.addWidget(self.n_field)
        layout.addWidget(self.max_tokens_field)
        layout.addWidget(self.repetition_penalty_field)
        layout.addWidget(self.font_size_combo)
        layout.addWidget(self.font_weight_combo)
        layout.addWidget(self.user_color_label)
        layout.addWidget(self.user_color_button)
        layout.addWidget(self.bot_color_label)
        layout.addWidget(self.bot_color_button)
        layout.addWidget(self.background_color_label)
        layout.addWidget(self.background_color_button)
        layout.addWidget(self.border_color_label)
        layout.addWidget(self.border_color_button)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def set_user_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.user_color_button.setStyleSheet(f"background-color: {color.name()};")
            self.chat_tab.set_user_color(color.name())

    def set_bot_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.bot_color_button.setStyleSheet(f"background-color: {color.name()};")
            self.chat_tab.set_bot_color(color.name())

    def set_background_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.background_color_button.setStyleSheet(f"background-color: {color.name()};")
            self.chat_tab.set_background_color(color.name())

    def set_border_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.border_color_button.setStyleSheet(f"background-color: {color.name()};")
            self.chat_tab.set_border_color(color.name())

    def accept(self):
        temperature = self.temperature_field.value()
        top_p = self.top_p_field.value()
        n = self.n_field.value()
        max_tokens = self.max_tokens_field.value()
        repetition_penalty = self.repetition_penalty_field.value()

        self.chat_tab.set_temperature(temperature)
        self.chat_tab.set_top_p(top_p)
        self.chat_tab.set_n(n)
        self.chat_tab.set_max_tokens(max_tokens)
        self.chat_tab.set_repetition_penalty(repetition_penalty)

        # Сохранение настроек
        self.save_user_settings()

        super().accept()

    def save_user_settings(self):
        settings = {
            "font_size": self.font_size_combo.currentText(),
            "font_weight": self.font_weight_combo.currentText(),
            "user_color": self.user_color_button.palette().button().color().name(),
            "bot_color": self.bot_color_button.palette().button().color().name(),
            "background_color": self.background_color_button.palette().button().color().name(),
            "border_color": self.border_color_button.palette().button().color().name(),
            "temperature": self.temperature_field.value(),
            "top_p": self.top_p_field.value(),
            "n": self.n_field.value(),
            "max_tokens": self.max_tokens_field.value(),
            "repetition_penalty": self.repetition_penalty_field.value()
        }
        with open("assets/settings.json", "w") as file:
            json.dump(settings, file)

    def load_user_settings(self):
        try:
            with open("assets/settings.json", "r") as file:
                settings = json.load(file)
                # Установка сохраненных параметров в виджеты
                self.font_size_combo.setCurrentText(settings.get("font_size", "16"))
                self.font_weight_combo.setCurrentText(settings.get("font_weight", "Bold"))
                self.temperature_field.setValue(settings.get("temperature", 0.7))
                self.top_p_field.setValue(settings.get("top_p", 0.1))
                self.n_field.setValue(settings.get("n", 1))
                self.max_tokens_field.setValue(settings.get("max_tokens", 99))
                self.repetition_penalty_field.setValue(settings.get("repetition_penalty", 1.0))

                # Применение сохраненных цветов к кнопкам
                user_color = extract_color(settings.get("user_color"))
                bot_color = extract_color(settings.get("bot_color"))
                background_color = extract_color(settings.get("background_color"))
                border_color = extract_color(settings.get("border_color"))

                set_button_color(self.user_color_button, user_color)
                set_button_color(self.bot_color_button, bot_color)
                set_button_color(self.background_color_button, background_color)
                set_button_color(self.border_color_button, border_color)

        except FileNotFoundError:
            # Обработка случая, когда файл настроек не найден
            pass

