from SQLiteWriter import SQLLiteWriter
from Table import SOATable, TransactionTable

sqlwriter = SQLLiteWriter("db.db")
for soa in sqlwriter.load_table(SOATable()):
    print(soa)
    for t in sqlwriter.load_table(TransactionTable(), "where soa_id==" + str(soa[0])):
        print(t)
