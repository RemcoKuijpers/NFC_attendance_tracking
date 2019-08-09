import PySimpleGUI as sg
import time
import subprocess

from Logger import Logger
from Database import DB

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
            self.window.Element("names").Update(data)

    def updateInfo(self, info):
        if info != self.old_info:
            self.old_info = info
            self.window.Element("info").Update(info)

if __name__ == "__main__":
    wg = WebGui()
    db = DB()
    db.infoText(" ")
    id = db.totalRows("persons") + 1 #Temp (delete when using reader)
    while True:
        db.__init__()
        wg.run(db.persons("present"), db.persons("info")[0][1])
        if wg.event is None:
            break
        if wg.event == "Nieuwe gebruiker aanmelden":
            process = subprocess.Popen("florence")
            naam = sg.PopupGetText("Leg RFID chip op de reader, en vul uw naam in.\nKlik daarna op Ok", "Vul naam in", location=(45,0))
            if naam != "" and naam is not None:
                # Add scan method here (id = reader.scan)
                db.insert("persons", id, naam)
                db.infoText('Gebruiker: ' + naam + ' met id ' + str(id) + ' is succesvol toegevoegd')
                id += 1 #Temp
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
                #Sla op
                db.infoText("Excel bestand is opgeslagen op USB-stick")
                time.sleep(1)
                process.terminate()
            else:
                db.infoText("Onjuist wachtwoord ingevoerd")
                time.sleep(1)
                process.terminate()
        db.__del__()
    wg.window.Close()
