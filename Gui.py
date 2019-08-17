import PySimpleGUI as sg
import time
import subprocess
import shutil
import os

from Logger import Logger
from Database import DB
from Reader import Reader

class WebGui():
    def __init__(self):
        self.old_data = []
        self.old_info = ''

        frame1_layout = [
                    [sg.Listbox(values=['','',''], size=(20,6), key="names")]
                ]

        frame2_layout = [
                    [sg.Text("Info", size=(22,5), font= "Courier 11", key="info", auto_size_text=True)]
                ]

        layout = [
                    [sg.Text("Actuele tijd", size=(200, 1), font= "Courier 65", key="tijd")],
                    [sg.Frame("Aanwezigen", frame1_layout), sg.Frame("Info", frame2_layout)],
                    [sg.Button("Nieuwe gebruiker aanmelden", enable_events=True, size=(33,1)), sg.Button("Afsluiten", enable_events=True, size=(7,1)), sg.Button("Opslaan", enable_events=True, size=(7,1))]
                ]

        self.window = sg.Window('Kloksysteem GUI', layout=layout, location=(0,0), size=(480,320), resizable=True, no_titlebar=False).Finalize()
        self.window.Maximize()

    def run(self, data, info):
        self.event, self.values = self.window.Read(timeout=1)
        self.updateTime()
        self.updateNames(data)
        self.updateInfo(info)

    def updateTime(self):
        t = time.strftime("%H:%M:%S")
        self.window.Element("tijd").Update(t)

    def updateNames(self, data):
        if data != self.old_data or data == []:
            self.old_data = data
            namelist = []
            for names in data:
                id, name = names
                namelist.append(names[1])
            self.window.Element("names").Update(namelist, scroll_to_index=len(namelist))

    def updateInfo(self, info):
        if info != self.old_info:
            self.old_info = info
            self.window.Element("info").Update(info)

if __name__ == "__main__":
    wg = WebGui()
    r = Reader()
    db = DB()
    l = Logger()
    db.infoText(" ")
    db.clearPresentTable()
    while True:
        db.__init__()
        wg.run(db.persons("present"), db.persons("info")[0][1])
        if wg.event is None:
            break
        if wg.event == "Nieuwe gebruiker aanmelden":
            process = subprocess.Popen("florence")
            naam = sg.PopupGetText("Leg RFID chip op de reader, en vul uw naam in.\nKlik daarna op Ok", "Vul naam in", location=(45,0))
            if naam != "" and naam is not None:
                r.__init__()
                uid = r.getUID()
                if uid is not None:
                    db.insert("persons", uid, naam)
                    db.infoText('Gebruiker: ' + naam + ' met id ' + uid + ' is succesvol toegevoegd')
                    process.terminate()
                    while r.getUID() is not None:
                        pass
                else:
                    db.infoText("Gebruiker niet toegevoegd, geen kaart geplaatst")
                    time.sleep(1)
                    process.terminate()
            else:
                db.infoText("Geen gebruiker toegevoegd")
                time.sleep(1)
                process.terminate()

        if wg.event == "Afsluiten":
            process = subprocess.Popen("florence")
            password = sg.PopupGetText("Geef wachtwoord om applicatie af te sluiten", "Vul wachtwoord in", location=(45,0))
            if password == "vdeboekel":
                time.sleep(1)
                process.terminate()
                break
            else:
                db.infoText("Onjuist wachtwoord ingevoerd")
                time.sleep(1)
                process.terminate()

        if wg.event == "Opslaan":
            process = subprocess.Popen("florence")
            password = sg.PopupGetText("Geef wachtwoord om excel bestand op USB-stick op te slaan", "Vul wachtwoord in", location=(45,0))
            if password == "vdeboekel":
                usb = os.popen('ls /media/pi').read()
                usb = usb.rstrip()
                shutil.rmtree("/home/pi/"+usb+"/Log", ignore_errors=True)
                if usb is None or usb == "":
                    db.infoText("Geen usb stick gedetecteerd")
                else:
                    if os.path.exists("/media/pi/"+usb+"/Log"):
                        shutil.rmtree("/media/pi/"+usb+"/Log")
                    shutil.copytree("/home/pi/NFC_attendance_tracking/Log", ("/media/pi/"+usb+"/Log"))
                    db.infoText("Excel bestand is opgeslagen op USB-stick")
                time.sleep(1)
                process.terminate()
            else:
                db.infoText("Onjuist wachtwoord ingevoerd")
                time.sleep(1)
                process.terminate()

        actId = r.getUID()
        if actId is not None and wg.event != "Nieuwe gebruiker aanmelden":
            if db.isIdPresent(actId) == False:
                l.clockIn(actId)
                while r.getUID() is not None:
                    pass
            else:
                l.clockOut(actId)
                while r.getUID() is not None:
                    pass
        else:
            r.__init__()

        db.__del__()
    wg.window.Close()
