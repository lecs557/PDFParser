import sys
from PyQt6 import QtWidgets, uic


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("test.ui", self)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())
