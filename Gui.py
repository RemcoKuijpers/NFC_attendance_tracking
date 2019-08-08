import PySimpleGUI as sg
import time

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
                    [sg.Text("Info", size=(15,5), font= "Courier 15", key="info", auto_size_text=True)]
                ]

        layout = [
                    [sg.Text("Actuele tijd", size=(200, 1), font= "Courier 65", key="tijd")],
                    [sg.Frame("Aanwezigen", frame1_layout), sg.Frame("Info", frame2_layout)],
                    [sg.Button("Nieuwe gebruiker aanmelden", enable_events=True, size=(91,1))]
                ]

        self.window = sg.Window('Kloksysteem GUI', layout=layout, location=(0,0), size=(480,320), keep_on_top=True, resizable=True, no_titlebar=True).Finalize()
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
    id = db.totalRows("persons") + 1 #Temp
    while True:
        db.__init__()
        wg.run(db.persons("present"), db.persons("info")[0][1])
        if wg.event is None:
            break
        if wg.event == "Nieuwe gebruiker aanmelden":
            naam = sg.PopupGetText("Leg RFID chip op de reader, en vul uw naam in, klik daarna op Ok", "Vul naam in")
            # Add scan method here
            db.insert("persons", id, naam)
            db.infoText('Gebruiker: ' + naam + ' met id ' + str(id) + ' is succesvol toegevoegd') #Temp
            id += 1 #Temp
        db.__del__()
    wg.window.Close()