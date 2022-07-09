import PySimpleGUI as sg
from SQLiteWriter import SQLLiteWriter
from Table import SOATable, TransactionTable
from GUIElement import SOAElement, TransactionTableRowElement, TransactionTableElement, YearElement, OverviewElement

sqlwriter = SQLLiteWriter("db.db")
tabs = []
for year in range(2014, 2023):
    tabContent = []
    for soa in sqlwriter.load_table(SOATable(), "where soa_date like '%"+str(year)+"%'"):
        transactions = []
        for t in sqlwriter.load_table(TransactionTable(), "where soa_id==" + str(soa[0])+" order by transaction_date"):
            transactions.append(TransactionTableRowElement(t))
        tabContent.append(SOAElement(soa, TransactionTableElement(transactions)))
    tabs.append(YearElement(str(year), tabContent))
layout = OverviewElement(tabs).get_layout()

# Create the window
window = sg.Window("Demo", layout, location=(410, 210))

open_soa = 0
# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break
    elif event:
        print(event)
        layout.insert(3, sg.Text("INSERT", key="i"))
        window.Refresh()


window.close()