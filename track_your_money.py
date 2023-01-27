import sys
from PyQt6 import QtWidgets

import GUIElement
from SQLiteWriter import SQLLiteWriter

app = QtWidgets.QApplication([])
sqlwriter = SQLLiteWriter("finanzen.db")

widget = GUIElement.buildApp(sqlwriter)
widget.resize(800, 600)
widget.show()

sys.exit(app.exec())
