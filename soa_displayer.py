import PySimpleGUI as sg
from SQLiteWriter import SQLLiteWriter
from Table import SOATable, TransactionTable
from GUIElement import SOAElement, TransactionTableRowElement, TransactionTableElement

sqlwriter = SQLLiteWriter("db.db")
tabs = []
for year in range(2014, 2023):
    tabContent = []
    for soa in sqlwriter.load_table(SOATable(), "where soa_date like '%"+str(year)+"%'"):
        transactions = []
        for t in sqlwriter.load_table(TransactionTable(), "where soa_id==" + str(soa[0])):
            transaction = TransactionTableRowElement(t)
            transactions.append(transaction)
        tableElement = TransactionTableElement(transactions)
        soaDiv = SOAElement(soa, tableElement)
        tabContent.append(soaDiv.get_layout())
    tab = [sg.Tab(str(year), tabContent)]
    tabs.append(tab)

layout = [[sg.TabGroup(tabs)]]

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
        if open_soa:
            print("delete")
            window.extend_layout(window["table"+str(open_soa)], [[]])
        print(event)
        open_soa += 1
        window.extend_layout(window[event], [[sg.Text("show", key="table"+str(open_soa))]])


window.close()