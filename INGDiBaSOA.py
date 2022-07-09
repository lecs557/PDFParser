import re


class INGDiBaSOA:
    datePattern = re.compile("\d{2}\.\d{2}\.\d{4}")

    def __init__(self):
        self.transactions = []
        self.date = None
        self.new = None
        self.old = None
        self.newY = None
        self.oldY = None
        self.valid = None

    def process(self, x, y, text):
        if self.oldY and -2 < self.oldY - y < 2:
            self.old = int(text.replace(".", "").replace(",", "").replace("Euro", ""))
            self.oldY = None
        if self.newY and -2 < self.newY - y < 2:
            self.new = int(text.replace(".", "").replace(",", "").replace("Euro", ""))
            self.newY = None
        if "Alter Saldo" in text:
            self.oldY = y
        if "Neuer Saldo" in text and x > 200:
            self.newY = y
        if self.datePattern.match(text) and x > 200 and not self.date:
            self.date = text
        self.get_transaction_by_y(y).process(x, y, text)

    def get_transaction_by_y(self, y):
        for transaction in self.transactions:
            if transaction.lastY and (0 < transaction.lastY - y < 15 or -5 <= transaction.y - y < 15):
                print("ALTE TRANSACTION %s" % transaction.y)
                return transaction
        t = Transaction(y)
        print("NEUE TRANSACTION %s" % y)
        self.transactions.append(t)
        return t

    def clear(self):
        rem = True
        while rem:
            rem = False
            for transaction in self.transactions:
                if not (transaction.date and transaction.subject and transaction.balance):
                    self.transactions.remove(transaction)
                    rem = True

    def new_page(self):
        for transaction in self.transactions:
            transaction.y = None
            transaction.lastY = None

    def validate(self):
        sum = 0
        for t in self.transactions:
            sum += t.balance
        if self.new - self.old == sum:
            self.valid = 1
        else:
            self.valid = 0


class Transaction:
    datePattern = re.compile("\d{2}\.\d{2}\.\d{4}")

    def __init__(self, y):
        self.date = None
        self.balance = None
        self.subject = None
        self.y = y
        self.lastY = y

    def process(self, x, y, text):
        print(text)
        if self.datePattern.match(text) and self.y == y:
            self.date = text
        if 100 < x < 200 and self.lastY - y < 15:
            if not self.subject:
                self.subject = text
            else:
                self.subject += "\n" + text
            self.lastY = y
        elif 400 < x < 600 and self.y == y:
            try:
                self.balance = int(text.replace(".", "").replace(",", ""))
            except Exception as e:
                self.y = None
                self.lastY = None
