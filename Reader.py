from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.ATR import ATR
from smartcard.CardType import AnyCardType
import smartcard
import sys

from Database import DB

class Reader():
    def __init__(self):
        self.db = DB()
        try:
            r = readers()
            reader = r[0]
            self.connection = reader.createConnection()
            self.connection.connect()
        except smartcard.Exceptions.NoCardException:
            #self.db.infoText("No card detected")
            pass

    def getCardInfo(self):
        print("###Tag Info###")
        atr = ATR(self.connection.getATR())
        hb = toHexString(atr.getHistoricalBytes())
        cardname = hb[-17:-12]
        cardnameMap = {
            "00 01": "MIFARE Classic 1K",
            "00 02": "MIFARE Classic 4K",
            "00 03": "MIFARE Ultralight",
            "00 26": "MIFARE Mini",
            "F0 04": "Topaz and Jewel",
            "F0 11": "FeliCa 212K",
            "F0 11": "FeliCa 424K"
        }
        name = cardnameMap.get(cardname, "unknown")
        print("Card Name: "+ name)
        print("T0 supported: ", atr.isT0Supported())
        print("T1 supported: ", atr.isT1Supported())
        print("T15 suppoerted: ", atr.isT15Supported())
        
    def getUID(self):
        try:
            data, sw1, sw2 = self.connection.transmit([0xFF, 0xCA, 0x00, 0x00, 0x00])
            uid = toHexString(data)
            if (sw1, sw2) == (0x90, 0x0):
                print("Card Id: " + uid)
                return str(uid)
            elif (sw1, sw2) == (0x63, 0x0):
                pass
        except smartcard.Exceptions.CardConnectionException:
            #self.db.infoText("No card detected")
            #print("No card detected")
            pass
