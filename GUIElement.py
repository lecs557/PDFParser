from PyQt6 import QtWidgets, QtGui


class SOAElement(QtWidgets.QWidget):
    def __init__(self, soa, show_element):
        super().__init__()
        self.soa = soa
        self.showEl = show_element
        self.soaEl = None
        self.color = "red"
        if self.soa[4]:
            self.color = "green"
        self.button = QtWidgets.QPushButton(str(soa[1]))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.toggle_show)


    def toggle_show(self):
        self.layout.addWidget(self.showEl)


class TransactionTableElement(QtWidgets.QTableView):
    def __init__(self, transaction_els):
        super().__init__()
        self.transaction_els = transaction_els
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(["date", "subject", "balance"])
        self.setModel(model)
        for t in self.transaction_els:
            model.appendRow(t.get())
        self.setFixedHeight(200)

class TransactionTableRowElement:
    def __init__(self, transaction):
        self.transaction = transaction

    def get(self):
        return [QtGui.QStandardItem(str(self.transaction[2])),
                QtGui.QStandardItem(str(self.transaction[3])),
                QtGui.QStandardItem(str(self.transaction[4]))]


class YearElement(QtWidgets.QWidget):
    def __init__(self, year, soa_els):
        super().__init__()
        self.year = year
        self.soa_els = soa_els
        self.layout = QtWidgets.QVBoxLayout(self)
        for t in self.soa_els:
            self.layout.addWidget(t)


class OverviewElement(QtWidgets.QWidget):
    def __init__(self, year_els):
        super().__init__()
        self.year_els = year_els
        self.tabs = QtWidgets.QTabWidget()
        for t in self.year_els:
            self.tabs.addTab(t, t.year)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tabs)

