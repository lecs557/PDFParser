import sys
from PyQt6 import QtWidgets
from SQLiteWriter import SQLLiteWriter
from Table import SOATable, TransactionTable
from GUIElement import SOAElement, TransactionTableRowElement, TransactionTableElement, YearElement, OverviewElement, SumElement


app = QtWidgets.QApplication([])
sum = SumElement()
sqlwriter = SQLLiteWriter("db.db")
tabs = []
for year in range(2014, 2023):
    tabContent = []
    for soa in sqlwriter.load_table(SOATable(), "where soa_date like '%" + str(year) + "%' order by file_name"):
        transactions = []
        for t in sqlwriter.load_table(TransactionTable(),
                                      "where soa_id==" + str(soa[0]) + " order by transaction_date"):
            sum.append_transaction_to_chart(t)
            transactions.append(TransactionTableRowElement(t))
        tabContent.append(SOAElement(soa, TransactionTableElement(transactions)))
    tabs.append(YearElement(str(year), tabContent))
widget = OverviewElement(tabs, sum)


widget.resize(800, 600)
widget.show()

sys.exit(app.exec())
