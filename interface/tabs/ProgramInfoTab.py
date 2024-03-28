from PySide6 import QtWidgets, QtCore


class ProgramInfoTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        # Create widgets for program information tab
        label = QtWidgets.QLabel("Это таб с информацией о программе")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Layout for program information tab
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
