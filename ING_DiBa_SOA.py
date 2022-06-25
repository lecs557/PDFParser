import re

class ING_DiBa_SOA:
    datePattern = re.compile("\d{2}\.\d{2}\.\d{4}")

    def __init__(self):
        self.transactions = []
        self.date = None
        self.new = None
        self.old = None
        self.newY = None
        self.oldY = None

    def process(self, x, y, text):
        if self.oldY and -2 < self.oldY - y < 2:
            self.old = int(text.replace(".", "").replace(",", "").replace("Euro", ""))
            self.oldY = None
        if self.newY and -2 < self.newY - y < 2:
            self.new = int(text.replace(".", "").replace(",", "").replace("Euro", ""))
            self.newY = None
        if "Alter Saldo" in text:
            self.oldY = y
        if "Neuer Saldo" in text:
            self.newY = y
        if self.datePattern.match(text) and x > 200 and not self.date:
            self.date = text
        self.getTransactionByY(y).process(x, y, text)

    def getTransactionByY(self, y):
        for transaction in self.transactions:
            if transaction.lastY and transaction.lastY - y < 15:
                return transaction
        t = Transaction(y)
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

    def newPage(self):
        for transaction in self.transactions:
            transaction.y = None
            transaction.lastY = None

    def validate(self):
        sum = 0
        for t in self.transactions:
            sum += t.balance
        if self.new - self.old == sum:
            print("Valid")
        else:
            print("%s %s" % (sum, self.new - self.old))
            print("invalid")


class Transaction:
    datePattern = re.compile("\d{2}\.\d{2}\.\d{4}")

    def __init__(self, y):
        self.date = None
        self.balance = None
        self.subject = None
        self.y = y
        self.lastY = y

    def process(self, x, y, text):
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
            except:
                self.y = None
                self.lastY = None
