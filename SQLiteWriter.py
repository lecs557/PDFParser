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
       # print(select+" "+where)
        cur = self.conn.cursor()
        cur.execute(select+" "+where)
        res = cur.fetchall()
        self.conn.commit()
        self.disconnect()
        return res

    def update_if_different(self, table, keys, values, id):
        self.connect()
        select = "select "
        update = "update " + table.get_tablename()
        set = "set "
        i = 0
        for x in keys:
            select += x
            set += x + "=" + str(values[i])
            i = i + 1
            if i != len(keys):
                select += ","
                set += " and "
        select += " from "+table.get_tablename() + " where id==" + str(id)
        set += " where id==" + str(id)
        print(select)
        cur = self.conn.cursor()
        cur.execute(select)
        res = cur.fetchall()
        if len(res) == 1 and not res[0] == values:
            cur = self.conn.cursor()
            print(update + " " + set)
            cur.execute(update + " " + set)
            self.conn.commit()
        self.disconnect()

    def insert_if_does_not_exists(self, table, values, ignore=[]):
        self.connect()
        select = "select id from " + table.get_tablename()
        where = "where "
        insert = "insert into " + table.get_tablename() + "("
        valuesql = "values("
        i = -2
        for x in table.get_table_fields():
            i = i + 1
            if x.name == "id" or x.name in ignore:
                continue
            insert += x.name
            valuesql += "\"" + str(values[i]) + "\""
            where += x.name + " == \"" + str(values[i]) + "\""
            if i+2 != len(table.get_table_fields()):
                insert += ","
                valuesql += ","
                where += " AND "
        insert += ")"
        valuesql += ")"
        print(select + " " + where)
        cur = self.conn.cursor()
        cur.execute(select + " " + where)
        res = cur.fetchall()
        if len(res) == 1:
            id = res[0][0]
        elif len(res) == 0:
            print(insert + " " + valuesql)
            cur.execute(insert + " " + valuesql)
            cur.execute(select + " " + where)
            res = cur.fetchall()
            id = res[0][0]
        else:
            print("update multiple entries?")
            id = res[:][0]
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
        #print(sql)
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
