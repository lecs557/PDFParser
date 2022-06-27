class Table:

    def get_tablename(self):
        pass

    def get_table_fields(self):
        pass


class TableFields:

    def __init__(self, name, type, attribute):
        self.name = name
        self.type = type
        self.attribute = attribute


class SOATable(Table):
    def get_tablename(self):
        return "soa"

    def get_table_fields(self):
        temp = [TableFields("id", "integer", "not null primary key autoincrement"),
                TableFields("soa_date", "text", "not null"),
                TableFields("old", "integer", "not null"),
                TableFields("new", "integer", "not null"),
                TableFields("valid", "integer", "not null")]
        return temp
