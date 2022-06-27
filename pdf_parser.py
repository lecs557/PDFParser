import sys
import os
from pdfminer.layout import LAParams, LTTextLine, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from INGDiBaSOA import INGDiBaSOA
from SQLiteWriter import SQLLiteWriter
from Table import SOATable


print("PDF Parser")

sqlwriter = SQLLiteWriter("db.db")
sqlwriter.create_table(SOATable())
id = sqlwriter.insert(SOATable(), ["test_date", "0", "900", "1"])
print(id)
sys.exit()
for year in range(2014, 2015):
    folder = "/home/marcel/Marcel/Geld/ING_DiBa/Kontoauszüge/Bilanz "+str(year)
    print(folder)
    files = os.listdir(folder)
    files.sort()
    for file in files:
        print(file)
        pdfFileObj = open(folder+"/"+file, 'rb')
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        soa = INGDiBaSOA()
        pages = PDFPage.get_pages(pdfFileObj)
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
        soa.clear()
        print("DATUM: %s" % soa.date)
        print("ALT: %s" % soa.old)
        print("NEU: %s" % soa.new)
        for t in soa.transactions:
            print(t)
        soa.validate()
