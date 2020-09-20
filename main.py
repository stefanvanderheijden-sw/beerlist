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

backgroundCLR = "black"
backgroundCLR2 = "black"
selectCLR = "green2"
fontColorCLR = "green2"

try:
    GPIO.setup(BUTTON_TOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_BOTTOM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    clkLastState = GPIO.input(17)
except:
    print("not on RPI 2")

from gpiozero import Buzzer
import time
import datetime
from time import sleep
import tkinter as tk
import operator
import csv
import sys
from tkinter import font
from tkinter import ttk

buzzer = Buzzer(16)

window = tk.Tk()
window.attributes("-fullscreen", True)
window.configure(bg=backgroundCLR2)

topColumn = tk.Frame(window)
topColumn.pack()

leftColumn = tk.Frame(window,background=backgroundCLR2)
leftColumn.pack(side="left",padx=10)

rightColumn = tk.Frame(window, height="700",width="100",background=backgroundCLR2)
rightColumn.pack(side="right")
rightColumn.pack_propagate(0)

rightTopButtonFrame = tk.Frame(rightColumn,background=backgroundCLR)
rightBottomButtonFrame = tk.Frame(rightColumn,background=backgroundCLR)

topButtonVar = tk.StringVar()
bottomButtonVar = tk.StringVar()

rightTopButtonLabel = tk.Label(rightTopButtonFrame,textvariable=topButtonVar, width =  "15",height= "2", background=backgroundCLR, fg= fontColorCLR,)
rightBottomButtonLabel = tk.Label(rightBottomButtonFrame,textvariable=bottomButtonVar, width =  "15",height= "2", background=backgroundCLR, fg= fontColorCLR,)

rightTopButtonFrame.pack(side="top")
rightBottomButtonFrame.pack(side="bottom")

rightTopButtonLabel.pack()
rightBottomButtonLabel.pack()

topButtonVar.set("ONE BEER")
bottomButtonVar.set("MENU")

greeting = tk.Label(text="Hello, Tkinter")
counter = 0
selected = 0

housemates = []
labelList = []

menuOpen = False

def openMenu():
    menuWindow = tk.Toplevel()
    menuWindow.wm_title("Window")
    menuWindow.attributes("-fullscreen", True)
    menuWindow.configure(bg=backgroundCLR2)

    menuLeftColumn = tk.Frame(menuWindow,background=backgroundCLR2)
    menuLeftColumn.grid(padx=10)

    l = tk.Label(menuWindow, text="Input")
    l.grid(row=0, column=0)

    b = ttk.Button(menuWindow, text="Okay", command=menuWindow.destroy)
    b.grid(row=1, column=0)

    menuItems = []

    menuItems.append(menuItem("DELETE HOUSEMATE", "function", 0,menuLeftColumn))
    menuItems.append(menuItem("ADD HOUSEMATE", "function", 1,menuLeftColumn))
    menuItems.append(menuItem("RESET BEERCOUNT", "function", 2,menuLeftColumn))
    menuItems.append(menuItem("EXIT MENU", "function", 3,menuLeftColumn))

def buttonFunction():
    sys.exit()

B = tk.Button(topColumn, text ="Exit", command = buttonFunction)
B.pack()

def sortlist(list):
    list.sort(key=operator.attrgetter('name'))
    return list

def topButton(pin):
    global menuOpen
    if menuOpen == False:
        housemates[selected].addOneBeer()
        housemates[selected].drawLabelBeer()
        buzzer.beep(on_time=0.05, off_time=1, n=1, background=True)

def bottomButton(pin):
    global menuOpen
    if menuOpen == False:
        openMenu()
        menuOpen = True
    # housemates[selected].substractOneBeer()
    # housemates[selected].drawLabelBeer()
    # buzzer.beep(on_time=0.2, off_time=1, n=1, background=True)


def pinDetect(pin):
    clkState = GPIO.input(17)
    dtState = GPIO.input(27)
    
    global selected
    global clkLastState
    housemates[selected].deSelect()
 
    if dtState != clkState:
        buzzer.beep(on_time=0.001, off_time=1, n=1, background=True)
        selected -= 1
    else:
        selected += 1
        buzzer.beep(on_time=0.001, off_time=1, n=1, background=True)

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
        self.tallyVar = tk.StringVar(0)
        self.name = name
        self.beercount = beercount
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
        self.label = tk.Label(leftColumn, text=self.name, width =  "15",height= "1", fg= fontColorCLR, background=backgroundCLR, anchor="w", font = ("Liberation Mono",10))
        self.label.grid(row = self.row, column=1, sticky = "w",pady="4")

    def drawLabelBeer(self):
        self.labelBeer = tk.Label(leftColumn,width =  "4", textvariable=self.beerVar, fg= fontColorCLR, background=backgroundCLR,font = ("Liberation Mono",10))
        self.beerVar.set(str(self.beercount))
        self.labelBeer.grid(row = self.row, column=2)

        tempTally = ""

        for i in range(self.beercount):
            tempTally += "|"

        self.tallyVar.set(tempTally)
        self.labelTally = tk.Label(leftColumn, width =  "40",textvariable=self.tallyVar, anchor="w", fg= fontColorCLR, background=backgroundCLR)
        self.labelTally.grid(row = self.row, column=3)

    def drawBeers(self):
        # self.labelBeer.grid_forget()
        self.drawLabel()

    def selfDestruct(self):
        self.label.grid_forget()
        self.labelBeer.grid_forget()
    
    def select(self):
        self.label.config(bg=selectCLR)
        self.label.config(fg=backgroundCLR)

    def deSelect(self):
        self.label.config(bg=backgroundCLR)
        self.label.config(fg=fontColorCLR)

class menuItem:
    def __init__(self, name, function, row,parentFrame):
        self.name = name
        self.function = function
        self.row = row
        self.drawLabel()
        self.parentFrame = parentFrame

    def drawLabel(self):
        self.label = tk.Label(self.parentFrame, text=self.name, width =  "15",height= "1", fg= fontColorCLR, background=backgroundCLR, anchor="w", font = ("Liberation Mono",10))
        self.label.grid(row = self.row, column=1, sticky = "w",pady="4")

    def select(self):
        self.label.config(bg=selectCLR)
        self.label.config(fg=backgroundCLR)

    def deSelect(self):
        self.label.config(bg=backgroundCLR)
        self.label.config(fg=fontColorCLR)

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

# remove_housemate_csv("Stefan")
# remove_housemate_csv("A3")
# remove_housemate_csv("Bastian")
# remove_housemate_csv("Lara")
# remove_housemate_csv("Sven")
# remove_housemate_csv("House")

clkLastState = GPIO.input(17)
try:
    GPIO.add_event_detect(17, GPIO.RISING, callback=pinDetect, bouncetime=30)
    GPIO.add_event_detect(BUTTON_TOP, GPIO.FALLING, callback=topButton, bouncetime=300)
    GPIO.add_event_detect(BUTTON_BOTTOM, GPIO.FALLING, callback=bottomButton, bouncetime=300)
except:
    print("not currently running on a RPI 2")

window.mainloop()