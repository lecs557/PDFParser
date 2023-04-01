import sys
from PyQt6 import QtWidgets

app = QtWidgets.QApplication([])

import GUIElement

GUIElement.WindowManager.show_main()

sys.exit(app.exec())
