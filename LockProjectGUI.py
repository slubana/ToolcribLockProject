from PyQt5.QtWidgets import *
import sys
import RPi.GPIO as GPIO
from datetime import datetime
import time
import csv
from mfrc522 import SimpleMFRC522

#rfid code
reader = SimpleMFRC522()

#striker code
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
RELAY_4_GPIO = 7 #GPIO 4
GPIO.setwarnings(False)
GPIO.setup(RELAY_4_GPIO, GPIO.OUT) #setup


listOfTools = [   "Impact Driver",        "Grinder",    "Hammer Drill", "Drill Driver",    "Work Light",
                     "Rivet Tool",   "TRQ W Driver",           "SAWZA", "Circular Saw",   "Flood Light",
                  "Torque Wrench",     "Grease Gun",        "Band Saw",      "Battery",   "HYD Crimper",
                "Crossline Laser", "QA Welding Set",  "Ring Piler Set",       "Megger",          "Dial",    
                     "Hole Punch", "Belt FRQ Meter", "Circuit Tracker", "Crimping Set",   "IR Temp Gun",
                   "Router Motor",      "Fish Tape",   "Leak Detector",  "Reamer Bits", "Hole Saw Bits",  
                "Work Light Post"
]

lengthOfToolsList = len(listOfTools)
checkboxList = []
for i in range(lengthOfToolsList):
    checkboxList.append('self.checkbox' + str(i))

selectedTools = []
employee = ''
status = ''

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Toolcrib Sign In/Out")

        layout = QGridLayout()
        self.setLayout(layout)
        self.showMaximized()

        #checklist code
        row = 0
        column = 0
        for checkbox in checkboxList:
            index = checkboxList.index(checkbox) #saves the position of the element in list
            checkbox = QCheckBox(listOfTools[index]) #creates a checkbox with the associated text
            checkbox.toggled.connect(self.checkbox_toggled) #calls the toggled function which adds/removes selected items
            layout.addWidget(checkbox, row, column) #adds checkbox to the screen
            if index < 10:
                column = 0
            elif index > 9 and index < 20:
                column = 1
            else:
                column = 2
            if index == 10 or index == 20:
                row = 0
            else:
                row += 1
           
            checkboxList[index] = checkbox #replaces the str checkbox to object checkboxes to be used elsewhere
       
        #button code
        button = QPushButton("NEXT")
        button.clicked.connect(self.on_button_clicked)
        layout.addWidget(button,11,1)

    def checkbox_toggled(self):
        for checkbox in checkboxList:
            index = checkboxList.index(checkbox)
            if checkbox.isChecked():
                if listOfTools[index] not in selectedTools:
                    selectedTools.append(listOfTools[index])
            else:
                if listOfTools[index] in selectedTools:
                    selectedTools.remove(listOfTools[index])
   
    def on_button_clicked(self):
        self.cams = Window1()
        self.cams.show()
        self.close()

class Window1(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Toolcrib Sign In/Out")

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.showMaximized()

        label = QLabel('Are you taking or returning the items?')
        rbtn1 = QRadioButton('Taking')
        rbtn2 = QRadioButton('Returning')
       
        rbtn1.toggled.connect(self.on_radio_button_clicked)
        rbtn2.toggled.connect(self.on_radio_button_clicked)

        button = QPushButton("DONE")
        button.clicked.connect(self.on_done_button_clicked)
   
        layout.addWidget(label)
        layout.addWidget(rbtn1)
        layout.addWidget(rbtn2)
        layout.addWidget(button)

    def on_radio_button_clicked(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            global status
            status = radioBtn.text()


    def on_done_button_clicked(self):
        self.showMinimized()
        GPIO.output(RELAY_4_GPIO, GPIO.HIGH)
        print ("OPENED")
        time.sleep(3)
        print ("CLOSED")
        GPIO.output(RELAY_4_GPIO, GPIO.LOW)
        for tools in selectedTools:
            data = [str(datetime.now()), employee, tools, status]
            with open('/home/pi/Documents/logs.csv','a',encoding='UTF8',newline='') as logs:
                csv_writer = csv.writer(logs)
                csv_writer.writerow(data)
        self.close()
 
 
def RFCreader():
    while True:
        print ("Place card on reader")
        rfid, text = reader.read()
        with open('/home/pi/Documents/employee_info.csv','rt') as employee_info:
            csv_reader = csv.reader(employee_info, delimiter=',')
            for row in csv_reader:
                if row[1] == str(rfid):
                    employee = row[0]
                    return employee
def appExec():
    app = QApplication(sys.argv)
    employee = RFCreader()
    screen = Window()
    app.exec_()
    appExec()
 
sys.exit(appExec())
