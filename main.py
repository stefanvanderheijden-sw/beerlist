try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
except:
    print("not on RPI 1")


BUTTON_TOP = 20
BUTTON_BOTTOM = 21



try:
    GPIO.setup(BUTTON_TOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_BOTTOM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    clkLastState = GPIO.input(17)
except:
    print("not on RPI 2")

import time
import datetime
from time import sleep
import tkinter as tk
import operator
import csv



window = tk.Tk()
#window.attributes("-fullscreen", True)

leftColumn = tk.Frame(window)
leftColumn.pack(side="left")

greeting = tk.Label(text="Hello, Tkinter")
counter = 0
selected = 0

housemates = []
labelList = []

def sortlist(list):
    list.sort(key=operator.attrgetter('name'))
    return list

def topButton(pin):
    housemates[selected].addOneBeer()
    housemates[selected].drawLabelBeer()

def bottomButton(pin):
    housemates[selected].substractOneBeer()
    housemates[selected].drawLabelBeer()
    add_housemate_csv("Nieuw Housemate")


def pinDetect(pin):
    clkState = GPIO.input(17)
    dtState = GPIO.input(27)
    
    global selected
    global clkLastState
    housemates[selected].deSelect()
 
    if dtState != clkState:
        selected -= 1
    else:
        selected += 1

    if selected < 1:
        selected = 0

    if (selected+1) > len(housemates):
        selected = (len(housemates)-1)

    housemates[selected].select()

def refreshList():
    for widget in leftColumn.winfo_children():
        widget.destroy()
    global housemates
    housemates = sortlist(housemates)
    for i in range(len(housemates)):
        housemates[i].setRow(i)
        housemates[i].refreshLabel()
        window.rowconfigure(i, weight=1)
    refreshBeerList()
        
def refreshBeerList():
    for housemate in housemates:
        housemate.drawLabelBeer()

class housemate:
    def __init__(self, name, beercount):
        self.beerVar = tk.StringVar(0)
        self.name = name
        self.beercount = beercount
        self.label = tk.Label(leftColumn, text=self.name, width =  "15",height= "2", background="white", anchor="w")
        self.labelBeer = tk.Label(leftColumn, textvariable=self.beerVar)
        self.row = 0

    def addOneBeer(self):
        self.beercount += 1

    def substractOneBeer(self):
        self.beercount -= 1
    
    def setBeerCount(self, count):
        self.beercount = count

    def setRow(self, row):
        self.row = row

    def refreshLabel(self):
        #self.label.grid_forget()
        self.drawLabel()
    
    def drawLabel(self):
        self.label = tk.Label(leftColumn, text=self.name, width =  "15",height= "2", background="white", anchor="w")
        self.label.grid(row = self.row, column=1, sticky = "w")

    def drawLabelBeer(self):
        self.labelBeer = tk.Label(leftColumn, textvariable=self.beerVar)
        self.beerVar.set(str(self.beercount))
        self.labelBeer.grid(row = self.row, column=2)

    def drawBeers(self):
        # self.labelBeer.grid_forget()
        self.drawLabel()

    def selfDestruct(self):
        self.label.grid_forget()
        self.labelBeer.grid_forget()

    
    def select(self):
        self.label.config(bg="gray")

    def deSelect(self):
        self.label.config(bg="white")

def write_to_csv():
# the a is for append, if w for write is used then it overwrites the file
    with open('/home/pi/Script/Beerlist/BeerListData.csv', mode='a') as beerListData:
        beerList_write = csv.writer(beerListData, delimiter=',', quotechar='”', quoting=csv.QUOTE_MINIMAL)
        write_to_log = beerList_write.writerow(["Test object 1","Test object 2","Test object 3"])
    return(write_to_log)

def read_housemate_csv():
    global housemates
    tempCsvHousemates = []
    with open('/home/pi/Script/Beerlist/housemates.csv', mode='r') as housemates_csv:
        csv_reader = csv.reader(housemates_csv, delimiter=',')
        for row in csv_reader:
            tempCsvHousemates.append(row[0])
    
    for tempCsvHousemate in tempCsvHousemates:        
        exists = 0
        for oldhousemate in housemates:
            if oldhousemate.name == tempCsvHousemate:
                exists = 1
                print(oldhousemate.name + " already exists")
        if exists == 0:
            housemates.append(housemate(tempCsvHousemate,0))
        
    temphousemates = []
    for newhousemate in housemates:
        for tempCsvHousemate in tempCsvHousemates:
            print("comparing " +newhousemate.name + " with " + tempCsvHousemate)
            if tempCsvHousemate == newhousemate.name:
                print("found a housemate in the csv file with the same name")
                temphousemates.append(newhousemate)
    
    for tempmate in temphousemates:
        print(tempmate.name + "      " +str(tempmate.beercount))

    housemates = temphousemates
    refreshList()

          

def add_housemate_csv(name):
    exist = 0
    for housemate in housemates:
        if housemate.name == name:
            exist = 1
    if exist == 0:
        with open('/home/pi/Script/Beerlist/housemates.csv', mode='a') as housemates_csv:
            housemate_write = csv.writer(housemates_csv, delimiter=',', quotechar='”', quoting=csv.QUOTE_MINIMAL)
            housemate_write.writerow([name])
        housemates_csv.close()
    read_housemate_csv()  

def remove_housemate_csv(name):
    lines = list()
    with open('/home/pi/Script/Beerlist/housemates.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            for field in row:
                if field == name:
                    lines.remove(row)
    readFile.close
    with open('/home/pi/Script/Beerlist/housemates.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)

    writeFile.close
    read_housemate_csv()     

read_housemate_csv()

# add_housemate_csv("Stefan")
# add_housemate_csv("Stefan2")
# add_housemate_csv("Stefan3")



remove_housemate_csv("Stefan")
remove_housemate_csv("A3")
remove_housemate_csv("Bastian")
remove_housemate_csv("Lara")
remove_housemate_csv("Sven")
remove_housemate_csv("House")



clkLastState = GPIO.input(17)
try:
    GPIO.add_event_detect(17, GPIO.RISING, callback=pinDetect, bouncetime=30)
    GPIO.add_event_detect(BUTTON_TOP, GPIO.FALLING, callback=topButton, bouncetime=300)
    GPIO.add_event_detect(BUTTON_BOTTOM, GPIO.FALLING, callback=bottomButton, bouncetime=300)
except:
    print("not currently running on a RPI 2")

window.mainloop()