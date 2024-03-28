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

        # Create OK and Cancel buttons
        self.ok_button = QtWidgets.QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        # Set window opacity
        self.setWindowOpacity(0.5)

        # Create labels for input fields
        self.temperature_label = QtWidgets.QLabel("Temperature:")
        self.top_p_label = QtWidgets.QLabel("Top P:")
        self.n_label = QtWidgets.QLabel("N:")
        self.max_tokens_label = QtWidgets.QLabel("Max Tokens:")
        self.repetition_penalty_label = QtWidgets.QLabel("Repetition Penalty:")

        layout = QtWidgets.QVBoxLayout()
        # Add labels to the layout
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.temperature_field)
        layout.addWidget(self.top_p_label)
        layout.addWidget(self.top_p_field)
        layout.addWidget(self.n_label)
        layout.addWidget(self.n_field)
        layout.addWidget(self.max_tokens_label)
        layout.addWidget(self.max_tokens_field)
        layout.addWidget(self.repetition_penalty_label)
        layout.addWidget(self.repetition_penalty_field)
        self.setLayout(layout)

    def accept(self):
        self.chat_tab.temperature = self.temperature_field.value()
        self.chat_tab.top_p = self.top_p_field.value()
        self.chat_tab.n = self.n_field.value()
        self.chat_tab.max_tokens = self.max_tokens_field.value()
        self.chat_tab.repetition_penalty = self.repetition_penalty_field.value()
        super().accept()