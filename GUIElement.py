from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis


class SOAElement(QtWidgets.QWidget):
    def __init__(self, soa, show_element):
        super().__init__()
        self.soa = soa
        self.showEl = show_element
        self.color = "red"
        if self.soa[4]:
            self.color = "green"
        self.button = QtWidgets.QPushButton(str(soa[1]))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.toggle_show)
        self.layout.setSpacing(0)
        self.click = False

    def toggle_show(self):
        self.click = not self.click
        if self.click:
            self.layout.addWidget(self.showEl)
        else:
            self.layout.itemAt(1).widget().setParent(None)


class TransactionTableElement(QtWidgets.QTableView):
    def __init__(self, transaction_els):
        super().__init__()
        self.transaction_els = transaction_els
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["date", "subject", "balance"])
        self.setModel(self.model)
        for t in self.transaction_els:
            self.model.appendRow(t.get())
        self.setWordWrap(True)
        self.resizeColumnToContents(1)
        self.setFixedHeight(200)
        self.selectionModel().selectionChanged.connect(self.sel_change)

    def sel_change(self, s, d):
        row = s.indexes()[0].row()
        col = s.indexes()[0].column()
        if col == 1:
            self.resizeRowToContents(row)
        else:
            self.setRowHeight(row, 10)
        print(self.transaction_els[row].transaction[3])


class TransactionTableRowElement:
    def __init__(self, transaction):
        self.transaction = transaction

    def get(self):
        date = QtGui.QStandardItem(str(self.transaction[2]))
        f = QtGui.QFont()
        f.setPointSizeF(13)
        date.setFont(f)
        subject = QtGui.QStandardItem(str(self.transaction[3]))
        subject.setFont(f)
        balance = QtGui.QStandardItem(str(self.transaction[4])[:-2] + "," + str(self.transaction[4])[-2:] + "€")
        balance.setFont(f)
        if self.transaction[4] > 0:
            balance.setForeground(QtGui.QColor(0, 155, 0))
        else:
            balance.setForeground(QtGui.QColor(155, 0, 0))
        return [date, subject, balance]


class YearElement(QtWidgets.QWidget):
    def __init__(self, year, soa_els):
        super().__init__()
        self.year = year
        self.soa_els = soa_els
        self.layout = QtWidgets.QVBoxLayout(self)
        for t in self.soa_els:
            self.layout.addWidget(t)
        self.layout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding))


class SumElement(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.sum = 0
        self.layout = QtWidgets.QVBoxLayout(self)
        self.series = QLineSeries()

    def append_transaction_to_chart(self, t):
        self.sum = self.sum + t[4]/100
        d = t[2].split(".")
        date = str(d[2]) + str(d[1]) + str(d[0]) + "0000"
        self.series.append(QtCore.QDateTime.fromString(date, "yyyyMMddhhmm").toMSecsSinceEpoch(), self.sum)

    def plot(self):
        chart = QChart()
        chart.addSeries(self.series)
        ax = QDateTimeAxis()
        ax.setFormat("MMM yyyy")
        ay = QValueAxis()
        chart.addAxis(ax, QtCore.Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(ay, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(ax)
        self.series.attachAxis(ay)
        self.layout.addWidget(QChartView(chart))
        self.layout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding))


class OverviewElement(QtWidgets.QWidget):
    def __init__(self, year_els, sum_el):
        super().__init__()
        self.year_els = year_els
        self.tabs = QtWidgets.QTabWidget()
        for t in self.year_els:
            self.tabs.addTab(t, t.year)
        sum_el.plot()
        self.tabs.addTab(sum_el, "SUM")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tabs)

