import sys

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QCategoryAxis
from Parser import Parser
from SQLiteWriter import SQLLiteWriter
from Table import SOATable, TransactionTable

TABLE_FONT = QtGui.QFont()
TABLE_FONT.setPointSizeF(13)


class SOAElement(QtWidgets.QWidget):
    def __init__(self, soa, show_element):
        super().__init__()
        self.soa = soa
        self.show_el = show_element
        self.color = "yellow"
        if self.soa[4]:
            if soa[3] - soa[2] > 0:
                self.color = "green"
            else:
                self.color = "red"
        self.hbox = QtWidgets.QHBoxLayout()
        self.button = QtWidgets.QPushButton("show")
        self.button.setStyleSheet("background-color: " + self.color)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.hbox.addWidget(self.button)
        self.hbox.addWidget(formatted_lbl(soa[3] - soa[2]))
        self.layout.addLayout(self.hbox)
        self.button.clicked.connect(self.toggle_show)
        self.click = False

    def toggle_show(self):
        self.click = not self.click
        if self.click:
            self.layout.addWidget(self.show_el)
        else:
            self.layout.itemAt(1).widget().setParent(None)


class TransactionTableElement(QtWidgets.QTableView):
    def __init__(self, transaction_els):
        super().__init__()
        self.totalout = 0
        self.totalin = 0
        self.sum = 0
        self.transaction_els = transaction_els
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["date", "subject", "balance"])
        self.setModel(self.model)
        for t in self.transaction_els:
            self.model.appendRow(t.get())
            self.sum = self.sum + t.transaction[4]
            if t.transaction[4] < 0:
                self.totalout = self.totalout + t.transaction[4]
            else:
                self.totalin = self.totalin + t.transaction[4]
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


class TransactionTableRowElement:
    def __init__(self, transaction):
        self.transaction = transaction

    def get(self):
        date = QtGui.QStandardItem(str(self.transaction[2]))
        date.setFont(TABLE_FONT)
        subject = QtGui.QStandardItem(str(self.transaction[3]))
        subject.setFont(TABLE_FONT)
        balance = formatted_si(self.transaction[4])
        return [date, subject, balance]


class YearElement(QtWidgets.QWidget):
    def __init__(self, year, soa_els):
        super().__init__()
        self.totalout = 0
        self.totalin = 0
        self.sum = 0
        self.year = year
        self.soa_els = soa_els
        self.layout = QtWidgets.QVBoxLayout(self)
        for t in self.soa_els:
            self.totalout = self.totalout + t.show_el.totalout
            self.totalin = self.totalin + t.show_el.totalin
            self.sum = self.sum + + t.show_el.sum
            self.layout.addWidget(t)
        self.layout.addWidget(create_total_table(self.totalin, self.totalout, self.sum))
        self.layout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                                  QtWidgets.QSizePolicy.Policy.Expanding))


class SumElement(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.totalin = 0
        self.totalout = 0
        self.sum = 0
        self.max = 0
        self.groups = ["AMAZON", "BAFOEG", "Wertpa", "Dividen", "Gehalt", "Pflegevers"]
        self.years = []
        self.sums = []
        self.y = 0
        self.miny = 2014
        self.maxy = 2022
        self.layout = QtWidgets.QVBoxLayout(self)
        self.series = QLineSeries()

    def append_transaction_to_chart(self, t):
        self.sum = self.sum + t[4]
        if t[4] < 0:
            self.totalout = self.totalout + t[4]
        else:
            self.totalin = self.totalin + t[4]
        if self.sum > self.max:
            self.max = self.sum

        d = t[2].split(".")
        date = str(d[2]) + str(d[1]) + str(d[0]) + "0000"
        self.series.append(QtCore.QDateTime.fromString(date, "yyyyMMddhhmm").toMSecsSinceEpoch(), self.sum)

        if int(d[2]) != self.y:
            if not self.sums == []:
                self.years.append(self.sums)
            self.y = int(d[2])
            self.sums = [0] * len(self.groups)
        for i, val in enumerate(self.groups):
            if val in t[3]:
                self.sums[i] = self.sums[i] + t[4]

    def create_sumtable(self):
        self.years.append(self.sums)
        model = QtGui.QStandardItemModel()
        header = ["subject"]
        rows = [[] for i in range(0, len(self.groups))]
        for v in range(self.miny, self.maxy + 1):
            header.append(str(v))
        for i, gr in enumerate(self.groups):
            rows[i].append(QtGui.QStandardItem(gr))
            for sum_v in self.years:
                rows[i].append(formatted_si(sum_v[i]))
        model.setHorizontalHeaderLabels(header)
        for row in rows:
            model.appendRow(row)
        tv = QtWidgets.QTableView()
        tv.setModel(model)
        return tv

    def plot(self):
        chart = QChart()
        chart.addSeries(self.series)
        ax = QDateTimeAxis()
        ax.setFormat("MMM yyyy")
        ax.setMin(QtCore.QDateTime.fromString(str(self.miny), "yyyy"))
        ax.setMax(QtCore.QDateTime.fromString(str(self.maxy + 1), "yyyy"))
        ax.setTickCount(self.maxy - self.miny + 2)
        ay = SumAxis()
        ay.setMax((int(self.max / 500000) + 1) * 500000)
        chart.addAxis(ax, QtCore.Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(ay, QtCore.Qt.AlignmentFlag.AlignLeft)
        cv = QChartView(chart)
        self.series.attachAxis(ax)
        self.series.attachAxis(ay)
        self.layout.addWidget(cv)
        self.create_table()

    def create_table(self):
        self.layout.addWidget(create_total_table(self.totalin, self.totalout, self.sum))
        self.layout.addWidget(self.create_sumtable())
        self.layout.addItem(
            QtWidgets.QSpacerItem(4, 2, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding))


class SumAxis(QCategoryAxis):
    def __init__(self):
        super().__init__()
        for i in range(0, 45000000, 500000):
            self.append(str(i)[0:-5] + " " + str(i)[-3:] + ",00 €", i)
        f = QtGui.QFont()
        f.setPointSizeF(10)
        self.setTruncateLabels(False)
        self.setLabelsPosition(QCategoryAxis.AxisLabelsPosition.AxisLabelsPositionOnValue)
        self.setLabelsFont(f)


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


class MainElement(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.widget = None
        self.thread = QtCore.QThread()
        self.parser = Parser()

        self.parser.moveToThread(self.thread)

        self.parser.sn_parse.connect(self.parser.parse)

        self.thread.start()

        btn_show = QtWidgets.QPushButton("Show")
        btn_show.clicked.connect(self.showElement)

        btn_browse = QtWidgets.QPushButton("browse folder...")
        btn_browse.clicked.connect(self.getfile)

        self.txt_path = QtWidgets.QLabel("path")

        self.in_from = QtWidgets.QSpinBox(self)
        self.in_from.setMinimum(2014)
        self.in_from.setMaximum(2025)
        self.in_from.setValue(2014)

        self.in_to = QtWidgets.QSpinBox(self)
        self.in_to.setMinimum(2014)
        self.in_to.setMaximum(2025)
        self.in_to.setValue(2023)

        btn_parse = QtWidgets.QPushButton("Parse")
        btn_parse.clicked.connect(self.parse)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(2)
        self.layout.addWidget(btn_show)
        self.layout.addWidget(self.txt_path)
        self.layout.addWidget(btn_browse)
        self.layout.addWidget(self.in_from)
        self.layout.addWidget(self.in_to)
        self.layout.addWidget(btn_parse)
        self.layout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                                  QtWidgets.QSizePolicy.Policy.Expanding))

    def showElement(self):
        WindowManager.show_overview()

    def getfile(self):
        fname = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.txt_path.setText(fname)

    def parse(self):
        if self.txt_path.text() == "path":
            print("choose path")
            return
        self.parser.sn_parse.emit(self.in_from.text(), self.in_to.text(), self.txt_path.text())


class WindowManager:
    load = None
    main = MainElement()
    overView = None

    @staticmethod
    def show_load():
        WindowManager.compute()
        WindowManager.overView.resize(800, 600)
        WindowManager.overView.show()

    @staticmethod
    def show_main():
        WindowManager.main.resize(800, 600)
        WindowManager.main.show()

    @staticmethod
    def show_overview():
        WindowManager.compute()
        WindowManager.overView.resize(800, 600)
        WindowManager.overView.show()

    @staticmethod
    def compute():
        sqlwriter = SQLLiteWriter("finanzen.db")
        sum_tab = SumElement()
        orderFilename = lambda y: "where soa_date like '%" + str(y) + "%' order by file_name"
        orderDate = lambda d: "where soa_id==" + str(d) + " order by transaction_date"
        tabs = []
        # first and last year
        orderFile= "order by SUBSTRING(file_name,3,7)"
        allsoas = sqlwriter.load_table(SOATable(), orderFile)
        first = int(allsoas[0][5][3:7])
        last = int(allsoas[len(allsoas)-1][5][3:7])
        for year in range(first, last+1):
            tabContent = []
            for soa in sqlwriter.load_table(SOATable(), orderFilename(year)):
                transactions = []
                for t in sqlwriter.load_table(TransactionTable(), orderDate(soa[0])):
                    # add point in chart for each transaction
                    sum_tab.append_transaction_to_chart(t)
                    # add table row for each transaction
                    transactions.append(TransactionTableRowElement(t))

                # add table for each state of account
                tabContent.append(SOAElement(soa, TransactionTableElement(transactions)))

            # add tab for each year
            tabs.append(YearElement(str(year), tabContent))

        WindowManager.overView = OverviewElement(tabs, sum_tab)


def create_total_table(i, o, s):
    model = QtGui.QStandardItemModel()
    model.setHorizontalHeaderLabels(["Einnahmen", "Ausgaben", "Gesamt"])
    in_si = formatted_si(i)
    out_si = formatted_si(o)
    sum_si = formatted_si(s)
    model.appendRow([in_si, out_si, sum_si])
    tv = QtWidgets.QTableView()
    tv.setModel(model)
    tv.setFixedHeight(50)
    return tv


def formatted_si(v):
    si = QtGui.QStandardItem(str(v)[0:-5] + " " + str(v).zfill(3)[-5:-2] + "," + str(v).zfill(3)[-2:] + "€")
    si.setFont(TABLE_FONT)
    if v > 0:
        si.setForeground(QtGui.QColor(0, 155, 0))
    elif v < 0:
        si.setForeground(QtGui.QColor(155, 0, 0))
    return si


def formatted_lbl(v):
    lbl = QtWidgets.QLabel(str(v)[0:-5] + " " + str(v).zfill(3)[-5:-2] + "," + str(v).zfill(3)[-2:] + "€")
    lbl.setFont(TABLE_FONT)
    if v > 0:
        lbl.setStyleSheet("color:rgb(0, 155, 0)")
    elif v < 0:
        lbl.setStyleSheet("color:rgb(155, 0, 0)")
    return lbl
