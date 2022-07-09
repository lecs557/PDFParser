import PySimpleGUI as sg


class SOAElement:
    def __init__(self, soa, show_element):
        self.soa = soa
        self.showEl = show_element.get_layout()
        self.soaEl = None
        self.show = False

    def get_layout(self):
        color = "red"
        if self.soa[4]:
            color = "green"

        self.soaEl = sg.Text(str(self.soa[5]), text_color=color, font=('Helvetica', 20), enable_events=True, key=lambda: self.toggle_show())
        return [self.soaEl]

    def toggle_show(self):
        self.show = not self.show
        self.showEl.Update(visible=self.show)


class TransactionTableElement:
    def __init__(self, transaction_els):
        self.transaction_els = transaction_els

    def get_layout(self):
        heading = ["date", "subject", "balance"]
        values = []
        for t in self.transaction_els:
            values.append(t.get_layout())
        return sg.Table(values=values, headings=heading)


class TransactionTableRowElement:
    def __init__(self, transaction):
        self.transaction = transaction

    def get_layout(self):
        return [self.transaction[2], self.transaction[3], self.transaction[4]]


class YearElement:
    def __init__(self, year, soa_els):
        self.year = year
        self.soa_els = soa_els

    def get_layout(self):
        values = []
        for t in self.soa_els:
            values.append(t.get_layout())
        return [sg.Tab(self.year, values)]


class OverviewElement:
    def __init__(self, year_els):
        self.year_els = year_els

    def get_layout(self):
        values = []
        for t in self.year_els:
            values.append(t.get_layout())
        return [[sg.TabGroup(values)]]