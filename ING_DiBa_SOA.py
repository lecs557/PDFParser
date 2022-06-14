class ING_DiBa_SOA:
    tra = False
    sal = 0
    date = ""
    old = 0
    new = 2000
    transactions = []

    def process(self, x, y, text):
        if 500 < x < 504 and 678 < y < 682:
            date = text
            print('DATUM: %s' % date)
        elif 495 < x < 499 and 637 < y < 641:
            self.old = int(text.replace(".", "").replace(",","").replace("Euro",""))
            print('ALT: %s' % self.old)
        elif 486 < x < 490 and 625 < y < 629:
            self.new = int(text.replace(".", "").replace(",","").replace("Euro",""))
            print('NEU: %s' % self.new)
        elif self.tra:
            if "Neuer Saldo" in text:
                self.sal = y
            if self.sal > y:
                self.tra = False
        if self.tra:
            self.getTransactionByY(y).process(x, y, text)
        if "Valuta" in text:
            self.tra = True

    def getTransactionByY(self, y):
        if len(self.transactions) == 0:
            self.transactions.append(Transaction(y))
        for transaction in self.transactions:
            if -3 < transaction.lastY(y) - y < 15:
                return transaction
        t = Transaction(y)
        self.transactions.append(t)
        return t

    def validate(self):
        sum = 0
        for t in self.transactions:
            if t.date != "":
                sum += t.balance
        if self.new - self.old == sum:
            print("Valid")
        else:
            print("%s %s" %(sum, self.new - self.old))
            print("invalid")


class Transaction:
    date = ""
    subject = ""
    balance = 500

    def __init__(self, y):
        self.b = None
        self.s = None
        self.d = y

    def process(self, x, y, text):
        if 68 < x < 72:
            self.date = text
        elif 139 < x < 143:
            if not self.s:
                self.subject = text
            else:
                self.subject += "\n" + text
            self.s = y
        elif 520 < x < 530:
            self.b = y
            self.balance = int(text.replace(",", ""))

    def lastY(self, y):
        if self.s:
            if self.s - y < 0:
                return self.d
            return self.s
        return self.d
