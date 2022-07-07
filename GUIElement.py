import PySimpleGUI as sg


class SOAElement:
    def __init__(self, soa, show_element):
        self.soa = soa
        self.soaEl = None
        self.showEl = show_element
        self.show = False

    def get_layout(self):
        color = "red"
        if self.soa[4]:
            color = "green"

        self.soaEl = [sg.Text(str(self.soa[5]), text_color=color, font=('Helvetica', 20), enable_events=True, key=lambda :self.toggle_show())]
        return self.soaEl

    def toggle_show(self):
        return [[self.showEl]]


class TransactionTableElement:
    def __init__(self, rows):
        self.rows = rows

    def get_layout(self):
        heading = ["date", "subject", "balance"]
        values = []
        for t in self.rows:
            values.append(t.get_layout())

        return [sg.Table(values=values, headings=heading, key="table")]


class TransactionTableRowElement:
    def __init__(self, transaction):
        self.transaction = transaction

    def get_layout(self):
        return [self.transaction[2], self.transaction[3], self.transaction[4]]
