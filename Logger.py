import xlwt
import xlrd
from datetime import datetime, date
from collections import defaultdict
import time
import sys
import os.path

from Database import DB

class Logger():
    def __init__(self):
        self.db = DB()

        self.today = date.today()
        print("Date is: "+str(self.today))

        self.todayString = date.today().strftime("%B %d, %Y")
        self.db.insert('vars', 'string', self.todayString)
        self.db.insert('vars', 'today', str(self.today))

        if os.path.exists('Log/'+self.today.strftime("%B %d, %Y")+'.xls') is False:
            self.wb = xlwt.Workbook()
            self.sheet = self.wb.add_sheet(self.today.strftime("%B %d, %Y"), cell_overwrite_ok=True)
            self.sheet.write(0, 0, 'Naam')
            self.sheet.write(0, 1, 'Id')
            self.sheet.write(0, 2, 'Inkloktijd')
            self.sheet.write(0, 3, 'Uitkloktijd')
            self.sheet.write(0, 4, 'Gewerkte tijd')
            self.wb.save('Log/'+self.today.strftime("%B %d, %Y")+'.xls')

        self.inTime = {}
        self.nums = {}
        self.num = 1
        self.ids = []

    def clockIn(self, id):
        self.db.__init__()
        name = self.db.lookUpName(id)
        self.today = date.today()

        if str(date.today()) != self.db.lookUpTime('today'):
            print("new day")
            print(str(date.today()))
            self.db.insert('vars', 'today', str(self.today))
            print(self.db.lookUpTime('today'))
            self.createNewFile()


        if name is not None:
            self.sheet.write(self.num, 0, name)
            self.sheet.write(self.num, 1, id)
            self.inTime[id] = datetime.now()
            self.nums[id] = self.num
            self.sheet.write(self.num, 2, self.inTime[id].strftime("%d/%m/%Y %H:%M:%S"))

            self.wb.save('Log/'+self.today.strftime("%B %d, %Y")+'.xls')

            self.db.insert('present', id, name)
            self.db.infoText(name + ' is succesvol ingeklokt')
            self.num += 1


    def clockOut(self, id):
        self.db.__init__()
        name = self.db.lookUpName(id)
        self.today = date.today()

        if str(date.today()) != self.db.lookUpTime('today'):
            print("new day")
            self.db.insert('vars', 'today', str(self.today))
            self.createNewFile()

        if name is not None:
            self.db.deleteId('present', id)
            now = datetime.now() 
            diff = now - self.inTime[id]
            self.sheet.write(self.nums[id], 3, now.strftime("%d/%m/%Y %H:%M:%S"))
            self.sheet.write(self.nums[id], 4, str(diff))
            self.wb.save('Log/'+self.today.strftime("%B %d, %Y")+'.xls')
            self.db.infoText(name + ' is succesvol uitgeklokt')

        self.db.__del__()

    def createNewFile(self):
        print("ceating new file")
        self.lastDay = self.db.lookUpTime('string')
        self.wb.save('Log/'+self.lastDay+'.xls')
        wbr = xlrd.open_workbook('Log/'+self.lastDay+'.xls')
        sheet = wbr.sheet_by_index(0)
        names = [sheet.cell_value(col, 0) for col in range(sheet.nrows)]
        ids = [sheet.cell_value(col, 1) for col in range(sheet.nrows)]
        self.today = date.today()
        self.db.insert('vars', 'today', str(self.today))
        self.num = 1
        self.wb = xlwt.Workbook()
        self.sheet = self.wb.add_sheet(self.today.strftime("%B %d, %Y"), cell_overwrite_ok=True)
        print(names)
        if names is not None:
            for i, val in enumerate(names):
                self.sheet.write(i, 0, val)
            for j, wal in enumerate(ids):
                self.sheet.write(j, 1, wal)
        self.sheet.write(0, 0, 'Naam')
        self.sheet.write(0, 1, 'Id')
        self.sheet.write(0, 2, 'Inkloktijd')
        self.sheet.write(0, 3, 'Uitkloktijd')
        self.sheet.write(0, 4, 'Gewerkte tijd')
        self.wb.save('Log/'+self.today.strftime("%B %d, %Y")+'.xls')

if __name__ == "__main__":
    Logger1 = Logger()
    print("Start Logging ...")
    Logger1.clockIn('04 34 77 CA 30 4C 80')
    time.sleep(1)
    Logger1.clockIn('04 5E 51 D2 30 4C 80')
    time.sleep(1)
    Logger1.clockOut('04 34 77 CA 30 4C 80')
    time.sleep(1)
    Logger1.clockOut('04 5E 51 D2 30 4C 80')
    time.sleep(1)