import os
from PyQt6 import QtCore, QtWidgets
from pdfminer.layout import LAParams, LTTextLine, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from INGDiBaSOA import INGDiBaSOA
from SQLiteWriter import SQLLiteWriter
from Table import SOATable, TransactionTable


class Parser(QtCore.QObject):
    sn_parse = QtCore.pyqtSignal(str, str, str)

    def parse(self, rfrom, rto, path):
        sqlwriter = SQLLiteWriter("finanzen.db")
        sqlwriter.create_table(SOATable())
        sqlwriter.create_table(TransactionTable())

        print("PDF Parser")
        # build folder name for each year and parse each file
        for year in range(int(rfrom), int(rto)):
            folder = path + '/Bilanz ' + str(year)
            print(folder)
            if not os.path.exists(folder):
                print("does not exist")
                continue
            files = os.listdir(folder)
            files.sort()
            # parse pdfs of the given year
            for file in files:
                print("read file: " + file)
                pdfFileObj = open(folder + "/" + file, 'rb')
                resource_manager = PDFResourceManager()
                device = PDFPageAggregator(resource_manager, laparams=LAParams())
                interpreter = PDFPageInterpreter(resource_manager, device)
                pages = PDFPage.get_pages(pdfFileObj)

                # create object to store the pages' content into
                soa = INGDiBaSOA()
                for page in pages:
                    soa.new_page()
                    interpreter.process_page(page)
                    layout = device.get_result()
                    for lobj in layout:
                        if isinstance(lobj, LTTextBox):
                            for line in lobj:
                                if isinstance(line, LTTextLine):
                                    x, y, text = float(line.bbox[0]), float(line.bbox[3]), line.get_text().strip()
                                    soa.process(x, y, text)

                # make sure to keep only transactions with date, subject and balance
                soa.clear()
                # check if the soa's total is the sum of every transaction
                soa.validate()
                # insert soa with its transactions
                soa_id = sqlwriter.insert_if_does_not_exists(SOATable(), [soa.date, soa.old, soa.new, soa.valid, file],
                                                             ignore=["valid"])
                sqlwriter.update_if_different(SOATable(), ["valid"], (soa.valid,), soa_id)
                for t in soa.transactions:
                    ta_id = sqlwriter.insert_if_does_not_exists(TransactionTable(), [soa_id, t.date, t.subject, t.balance])
                if soa.valid:
                    print(file + " is valid")
                else:
                    print(file + " is invalid!! Please check!")


