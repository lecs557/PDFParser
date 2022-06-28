import sqlite3
from sqlite3 import Error


class SQLLiteWriter:

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def load_table(self, table, where=""):
        self.connect()
        select = "select "
        i = 0
        for x in table.get_table_fields():
            select += x.name
            i = i + 1
            if i != len(table.get_table_fields()):
                select += ","
        select += " from "+table.get_tablename()
        print(select+" "+where)
        cur = self.conn.cursor()
        cur.execute(select+" "+where)
        res = cur.fetchall()
        self.conn.commit()
        self.disconnect()
        return res

    def insert(self, table, values):
        self.connect()
        select = "select id from " + table.get_tablename()
        where = "where "
        sql = "insert into " + table.get_tablename() + "("
        valuesql = "values("
        i = 0
        for x in table.get_table_fields():
            if x.name == "id":
                continue
            sql += x.name
            valuesql += "\"" + str(values[i]) + "\""
            where += x.name + " == \"" + str(values[i]) + "\""
            i = i + 1
            if i + 1 != len(table.get_table_fields()):
                sql += ","
                valuesql += ","
                where += " AND "
        sql += ")"
        valuesql += ")"
        print(select + " " + where)
        cur = self.conn.cursor()
        cur.execute(select + " " + where)
        res = cur.fetchall()
        if len(res) == 1:
            id = res[0][0]
        else:
            print(sql + " " + valuesql)
            cur.execute(sql + " " + valuesql)
            cur.execute(select + " " + where)
            res = cur.fetchall()
            id = res[0][0]
        self.conn.commit()
        self.disconnect()
        return id

    def create_table(self, table):
        self.connect()
        sql = "create table if not exists " + table.get_tablename() + "("
        i = 0
        for x in table.get_table_fields():
            i = i + 1
            sql += x.name + " "
            sql += x.type + " "
            sql += x.attribute
            if i != len(table.get_table_fields()):
                sql += ",\n"
        sql += ")"
        print(sql)
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        self.disconnect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)

    def disconnect(self):
        if self.conn:
            self.conn.close()
