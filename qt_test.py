import random
from PyQt6 import QtWidgets

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.tabs = QtWidgets.QTabWidget()
        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    def magic(self):
        self.text.setText(random.choice(self.hello))

