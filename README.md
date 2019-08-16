# NFC_attendance_tracking
Attendance tracking by using NFC tags and a NFC card reader with a Raspberry Pi.
In this [README](https://github.com/RemcoKuijpers/NFC_attendance_tracking/blob/master/README.md) is explained how to get the project up and running. If you want know more about how the project works, you can check out the wiki. (the wiki is still in the making)

## Getting started
In this chapter is explained how to get the project up and running

### Hardware
In this chapter is explained which hardware is used for this project.
* [Raspberry Pi 3B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)
* [ACM122U NFC Reader](https://www.acs.com.hk/en/products/3/acr122u-usb-nfc-reader/)
* [3.5 Inch LCD Touchscreen module for RPi](http://www.lcdwiki.com/3.5inch_RPi_Display)
* [NTAG213 NFC Cards](https://www.bol.com/nl/p/nfc-tag-ntag213-cards/9200000076793632/)

### Prerequisites
In this chapter is explained which packages need to be installed.
* [PySimpleGUI](https://pypi.org/project/PySimpleGUI/)
* [sqlite3](https://docs.python.org/3/library/sqlite3.html)
* [xlwt](https://pypi.org/project/xlwt/)
* [xlrd](https://pypi.org/project/xlrd/)
* [pyscard](https://pyscard.sourceforge.io/)

## Installing
To clone this repository to your system run the following command:
```
git clone https://github.com/RemcoKuijpers/NFC_attendance_tracking.git
```
#### Running on boot up
If wou want to start the program on the bootup of the Raspberry Pi. You have to add the [Gui.desktop](https://github.com/RemcoKuijpers/NFC_attendance_tracking/blob/master/Gui.desktop) to the following folder on your Raspberry Pi:
```
/etc/xdg/autostart
```
