import xlwt
import xlrd
from datetime import datetime, date
import time
import sys

from Database import DB

class Logger():
    def __init__(self):
        self.db = DB()
        self.wb = xlwt.Workbook()
        self.today = date.today()
        self.sheets = {}
        self.day = 1
        self.sheets[self.day] = self.wb.add_sheet(self.today.strftime("%B %d, %Y"))
        self.sheets[self.day].write(0, 0, 'Naam')
        self.sheets[self.day].write(0, 1, 'Id')
        self.sheets[self.day].write(0, 2, 'Inkloktijd')
        self.sheets[self.day].write(0, 3, 'Uitkloktijd')
        self.sheets[self.day].write(0, 4, 'Gewerkte tijd')
        self.inTime = {}
        self.nums = {}
        self.num = 1
        self.ids = []

    def clockIn(self, id):
        name = self.db.lookUpName(id)

        if date.today() != self.today:
            wbr = xlrd.open_workbook('Log/test.xls')
            sheet = wbr.sheet_by_index(self.day - 1)
            names = [sheet.cell_value(col, 0) for col in range(sheet.nrows)]
            ids = [sheet.cell_value(col, 1) for col in range(sheet.nrows)]
            self.day += 1
            self.today = date.today()
            self.sheets[self.day] = self.wb.add_sheet(self.today.strftime("%B %d, %Y"))
            self.sheets[self.day].write(0, 2, 'Inkloktijd')
            self.sheets[self.day].write(0, 3, 'Uitkloktijd')
            self.sheets[self.day].write(0, 4, 'Gewerkte tijd')

            for i, val in enumerate(names):
                self.sheets[self.day].write(i, 0, val)
            for j, wal in enumerate(ids):
                self.sheets[self.day].write(j, 1, wal)

        if name is not None:
            self.db.insert('present', id, name)
            self.sheets[self.day].write(self.num, 0, name)
            self.sheets[self.day].write(self.num, 1, id)
            self.inTime[int(id)] = datetime.now()
            self.nums[int(id)] = self.num
            self.sheets[self.day].write(self.num, 2, self.inTime[int(id)].strftime("%d/%m/%Y %H:%M:%S"))
            self.wb.save('Log/test.xls')
            self.num += 1

            self.db.infoText(name + ' is succesvol ingeklokt')

    def clockOut(self, id):
        name = self.db.lookUpName(id)

        if date.today() != self.today:
            wbr = xlrd.open_workbook('Log/test.xls')
            sheet = wbr.sheet_by_index(self.day - 1)
            names = [sheet.cell_value(col, 0) for col in range(sheet.nrows)]
            ids = [sheet.cell_value(col, 1) for col in range(sheet.nrows)]
            self.day += 1
            self.today = date.today()
            self.sheets[self.day] = self.wb.add_sheet(self.today.strftime("%B %d, %Y"))
            self.sheets[self.day].write(0, 2, 'Inkloktijd')
            self.sheets[self.day].write(0, 3, 'Uitkloktijd')
            self.sheets[self.day].write(0, 4, 'Gewerkte tijd')
        
            for i, val in enumerate(names):
                self.sheets[self.day].write(i, 0, val)
            for j, wal in enumerate(ids):
                self.sheets[self.day].write(j, 1, wal)

        if name is not None:
            self.db.deleteId('present', id)

            now = datetime.now()
            diff = now - self.inTime[int(id)]
            self.sheets[self.day].write(self.nums[int(id)], 3, now.strftime("%d/%m/%Y %H:%M:%S"))
            self.sheets[self.day].write(self.nums[int(id)], 4, str(diff))
            self.wb.save('Log/test.xls')

            self.db.infoText(name + ' is succesvol uitgeklokt')


if __name__ == "__main__":
    Logger1 = Logger()
    Logger1.clockIn('1')
    time.sleep(5)
    Logger1.clockIn('2')
    time.sleep(3)
    Logger1.clockOut('1')
    time.sleep(5)
    Logger1.clockIn('2')
    time.sleep(4)