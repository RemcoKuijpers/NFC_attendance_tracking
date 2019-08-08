import sqlite3

class DB():
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.conn.execute('create table if not exists ' + 'persons' + ' (id integer PRIMARY KEY, name text)')
        self.conn.execute('create table if not exists ' + 'present' + ' (id integer PRIMARY KEY, name text)')
        self.conn.execute('create table if not exists ' + 'info' + ' (id integer PRIMARY KEY, info text)')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def totalRows(self, table):
        self.c.execute('select count(*) from ' + table)
        self.conn.commit()
        return self.c.fetchall()[0][0]

    def insert(self, table, id, name):
        try:
            self.c.execute('insert into ' + table + ' values (?,?)', (id, name))
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.infoText('Id is al in gebruik')

    def deleteId(self, table, id):
        self.c.execute('delete from ' + table + ' where id = ' + str(id))
        self.conn.commit()

    def clearPresentTable(self):
        self.c.execute('delete from present')
        self.conn.commit()

    def clearPersonsTable(self):
        self.c.execute('delete from persons')
        self.conn.commit()

    def persons(self, table):
        self.c.execute('select * from ' + table)
        self.conn.commit()
        return self.c.fetchall()

    def infoText(self, info):
        id = 1
        self.c.execute('delete from info')
        self.c.execute('insert into info values (?,?)', (id, info))
        self.conn.commit()

    def lookUpName(self, id):
        try:
            self.c.execute('select * from persons where id= ' + str(id))
            self.conn.commit()
            return self.c.fetchall()[0][1]
        except IndexError:
            self.infoText("Id niet gevonden, meldt u eerst aan")