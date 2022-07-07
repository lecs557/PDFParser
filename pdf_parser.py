import sys
import os
from pdfminer.layout import LAParams, LTTextLine, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from INGDiBaSOA import INGDiBaSOA
from SQLiteWriter import SQLLiteWriter
from Table import SOATable, TransactionTable


print("PDF Parser")
sqlwriter = SQLLiteWriter("db.db")
sqlwriter.create_table(SOATable())
sqlwriter.create_table(TransactionTable())
for year in range(2022, 2023):
    folder = "/home/marcel/Marcel/Geld/ING_DiBa/Kontoauszüge/Bilanz "+str(year)
    print(folder)
    files = os.listdir(folder)
    files.sort()
    for file in files:
        print(file)
        if "02.2022" in file:
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
            soa.validate()
            id = sqlwriter.insert_if_does_not_exists(SOATable(), [soa.date, soa.old, soa.new, soa.valid, file], ignore=["valid"])
            sqlwriter.update_if_different(SOATable(), ["valid"], (soa.valid,), id)
            for t in soa.transactions:
                pass
                #ta_id = sqlwriter.insert_if_does_not_exists(TransactionTable(), [id, t.date, t.subject, t.balance])
