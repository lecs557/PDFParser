from pdfminer.layout import LAParams, LTTextLine, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from ING_DiBa_SOA import ING_DiBa_SOA
import sys

print("PDF Parser")
if len(sys.argv) <= 1:
    print("no file")
else:
    print("filepath: " + sys.argv[1])

pdfFileObj = open(sys.argv[1], 'rb')

rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
soa = ING_DiBa_SOA()
pages = PDFPage.get_pages(pdfFileObj)

for page in pages:
    print('Processing next page...')
    interpreter.process_page(page)
    layout = device.get_result()
    for lobj in layout:
        if isinstance(lobj, LTTextBox):
            for line in lobj:
                if isinstance(line, LTTextLine):
                    x, y, text = float(line.bbox[0]), float(line.bbox[3]), line.get_text().strip()
                    soa.process(x, y, text)
for t in soa.transactions:
    if t.date != "":
        print(t.date)
        print(t.subject)
        print(t.balance)
soa.validate()