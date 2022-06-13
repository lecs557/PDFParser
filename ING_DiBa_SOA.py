class ING_DiBa_SOA:
    date = ""
    old = 0
    new = 2000
    transactions = []
    def process(self,x,y,text):
        if 500 < x and x < 504 and 678 < y and y < 682:
            date = text
            print('DATUM: %s' % date)
        else:
            print('At %r is text: %s' % ((x, y), text))

class Transaction:
    date = ""
    subject = ""
    balance = 500
    def process(self, x, y, text):
        print('At %r is text: %s' % ((x, y), text))