import json

from PySide6 import QtWidgets


class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, chat_tab):
        super().__init__()
        self.chat_tab = chat_tab
        self.setWindowOpacity(0.5)

        # Create input fields for parameters
        self.temperature_field = QtWidgets.QDoubleSpinBox()
        self.top_p_field = QtWidgets.QDoubleSpinBox()
        self.n_field = QtWidgets.QSpinBox()
        self.max_tokens_field = QtWidgets.QSpinBox()
        self.repetition_penalty_field = QtWidgets.QDoubleSpinBox()

        # Set initial values
        self.temperature_field.setValue(self.chat_tab.temperature)
        self.top_p_field.setValue(self.chat_tab.top_p)
        self.n_field.setValue(self.chat_tab.n)
        self.max_tokens_field.setValue(self.chat_tab.max_tokens)
        self.repetition_penalty_field.setValue(self.chat_tab.repetition_penalty)

        # Create font size combo box
        self.font_size_combo = QtWidgets.QComboBox()
        self.font_size_combo.addItems([str(size) for size in range(8, 31)])
        self.font_size_combo.setCurrentText("16")

        # Create font weight combo box
        self.font_weight_combo = QtWidgets.QComboBox()
        self.font_weight_combo.addItems(["Normal", "Bold"])
        self.font_weight_combo.setCurrentIndex(1)

        # Create message color labels and combo boxes
        self.user_color_label = QtWidgets.QLabel("User message color:")
        self.user_color_combo = QtWidgets.QComboBox()
        self.user_color_combo.addItems(["blue", "green", "red", "yellow", "cyan", "magenta"])
        self.user_color_combo.setCurrentIndex(0)

        self.bot_color_label = QtWidgets.QLabel("Bot message color:")
        self.bot_color_combo = QtWidgets.QComboBox()
        self.bot_color_combo.addItems(["blue", "green", "red", "yellow", "cyan", "magenta"])
        self.bot_color_combo.setCurrentIndex(1)

        # Create background color fields
        self.background_color_label = QtWidgets.QLabel("Background color:")
        self.background_color_combo = QtWidgets.QComboBox()
        self.background_color_combo.addItems(["black", "white", "gray", "blue", "green", "red"])
        self.background_color_combo.setCurrentIndex(0)

        # Create border color fields
        self.border_color_label = QtWidgets.QLabel("Border color:")
        self.border_color_combo = QtWidgets.QComboBox()
        self.border_color_combo.addItems(["black", "white", "gray", "blue", "green", "red"])
        self.border_color_combo.setCurrentIndex(1)

        # Create OK and Cancel buttons
        self.ok_button = QtWidgets.QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        # Create labels for input fields
        self.temperature_label = QtWidgets.QLabel("Temperature:")
        self.top_p_label = QtWidgets.QLabel("Top P:")
        self.n_label = QtWidgets.QLabel("N:")
        self.max_tokens_label = QtWidgets.QLabel("Max Tokens:")
        self.repetition_penalty_label = QtWidgets.QLabel("Repetition Penalty:")

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.temperature_label, 0, 0)
        layout.addWidget(self.temperature_field, 0, 1)
        layout.addWidget(self.top_p_label, 1, 0)
        layout.addWidget(self.top_p_field, 1, 1)
        layout.addWidget(self.n_label, 2, 0)
        layout.addWidget(self.n_field, 2, 1)
        layout.addWidget(self.max_tokens_label, 3, 0)
        layout.addWidget(self.max_tokens_field, 3, 1)
        layout.addWidget(self.repetition_penalty_label, 4, 0)
        layout.addWidget(self.repetition_penalty_field, 4, 1)

        layout.addWidget(QtWidgets.QLabel("Font size:"), 5, 0)
        layout.addWidget(self.font_size_combo, 5, 1)
        layout.addWidget(QtWidgets.QLabel("Font weight:"), 6, 0)
        layout.addWidget(self.font_weight_combo, 6, 1)
        layout.addWidget(self.user_color_label, 7, 0)
        layout.addWidget(self.user_color_combo, 7, 1)
        layout.addWidget(self.bot_color_label, 8, 0)
        layout.addWidget(self.bot_color_combo, 8, 1)
        layout.addWidget(self.background_color_label, 9, 0)
        layout.addWidget(self.background_color_combo, 9, 1)
        layout.addWidget(self.border_color_label, 10, 0)
        layout.addWidget(self.border_color_combo, 10, 1)
        layout.addWidget(self.ok_button, 11, 0)
        layout.addWidget(self.cancel_button, 11, 1)

        self.setLayout(layout)

    def accept(self):
        # Получение выбранных параметров
        font_size = int(self.font_size_combo.currentText())
        font_weight = "bold" if self.font_weight_combo.currentText() == "Bold" else "normal"
        user_color = self.user_color_combo.currentText()
        bot_color = self.bot_color_combo.currentText()
        background_color = self.background_color_combo.currentText()
        border_color = self.border_color_combo.currentText()
        temperature = self.temperature_field.value()
        top_p = self.top_p_field.value()
        n = self.n_field.value()
        max_tokens = self.max_tokens_field.value()
        repetition_penalty = self.repetition_penalty_field.value()

        # Применение настроек к ChatTab
        self.chat_tab.set_font_size(font_size)
        self.chat_tab.set_font_weight(font_weight)
        self.chat_tab.set_user_color(user_color)
        self.chat_tab.set_bot_color(bot_color)
        self.chat_tab.set_background_color(background_color)
        self.chat_tab.set_border_color(border_color)
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
            "user_color": self.user_color_combo.currentText(),
            "bot_color": self.bot_color_combo.currentText(),
            "background_color": self.background_color_combo.currentText(),
            "border_color": self.border_color_combo.currentText(),
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
                self.font_size_combo.setCurrentText(str(settings["font_size"]))
                self.font_weight_combo.setCurrentText(settings["font_weight"])
                self.user_color_combo.setCurrentText(settings["user_color"])
                self.bot_color_combo.setCurrentText(settings["bot_color"])
                self.background_color_combo.setCurrentText(settings["background_color"])
                self.border_color_combo.setCurrentText(settings["border_color"])
                self.temperature_field.setValue(settings["temperature"])
                self.top_p_field.setValue(settings["top_p"])
                self.n_field.setValue(settings["n"])
                self.max_tokens_field.setValue(settings["max_tokens"])
                self.repetition_penalty_field.setValue(settings["repetition_penalty"])
        except FileNotFoundError:
            # Обработка случая, когда файл настроек не найден
            pass
