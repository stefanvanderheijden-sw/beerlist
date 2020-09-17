
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

from time import sleep
import tkinter as tk
import operator

window = tk.Tk()
greeting = tk.Label(text="Hello, Tkinter")
counter = 0
selected = 0
clkLastState = GPIO.input(17)
housemates = []
labelList = []

def sortlist(list):
    list.sort(key=operator.attrgetter('name'))
    return list

def pinDetect(pin):
    global selected
    global clkLastState
    housemates[selected%10].deSelect()
 
    clkState = GPIO.input(17)
    # if clkState != clkLastState:
    dtState = GPIO.input(27)
    if dtState != clkState:
        selected += 1
    else:
        selected -= 1
        
    print(str(selected))

    clkLastState = clkState
    # global selected
    # housemates[selected].deSelect()

    # pin2 = GPIO.input(27)
    
    # if pin2:
    #     selected += 1
    #     if selected > 10:
    #         selected = 1

    # else:
    #     selected -= 1
    #     if selected < 1:
    #         selected = 10

    
    

def refreshList():
    global housemates
    housemates = sortlist(housemates)
    for i in range(len(housemates)):
        housemates[i].setRow(i)
        housemates[i].refreshLabel()
    refreshBeerList()
        

def refreshBeerList():
    for housemate in housemates:
        housemate.drawLabelBeer()

class housemate:
    def __init__(self, name, beercount):
        self.beerVar = tk.StringVar(0)
        self.name = name
        self.beercount = beercount
        self.label = tk.Label(window, text=self.name, width =  "15", background="white", anchor="w")
        self.labelBeer = tk.Label(window, textvariable=self.beerVar)
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
        self.label.grid_forget()
        self.drawLabel()
    
    def drawLabel(self):
        self.label.grid(row = self.row, column=1, sticky = "w")

    def drawLabelBeer(self):
        self.beerVar.set(str(self.beercount))
        self.labelBeer.grid(row = self.row, column=2)

    def drawBeers(self):
        self.labelBeer.grid_forget()
        self.drawLabel()

    def selfDestruct(self):
        global housemates
        
        self.label.grid_forget()
        self.labelBeer.grid_forget()

        housemates.pop(self.row)
    
    def select(self):
        self.label.config(bg="gray")

    def deSelect(self):
        self.label.config(bg="white")

housemates.append(housemate("Florine",0))
housemates.append(housemate("Starr & Lance",0))
housemates.append(housemate("A3",0))
housemates.append(housemate("Alex",0))
housemates.append(housemate("Martijn",0))
housemates.append(housemate("Abel",0))
housemates.append(housemate("Jonah",0))
housemates.append(housemate("Kalea",0))
housemates.append(housemate("Merel",0))
housemates.append(housemate("Stefan",0))
housemates.append(housemate("Johanna",0))
housemates.append(housemate("Salvador & Anita",0))
housemates.append(housemate("Lara",0))
housemates.append(housemate("Larisa",0))
housemates.append(housemate("Kyra & Wouter",0))
housemates.append(housemate("Bas",0))
housemates.append(housemate("Isa",0))
housemates.append(housemate("Barbara & Max",0))
housemates.append(housemate("Bianca",0))
housemates.append(housemate("Vita",0))
housemates.append(housemate("Marice",0))
housemates.append(housemate("Bastian",0))
housemates.append(housemate("Barbara jr",0))
housemates.append(housemate("Rik & Amber",0))
housemates.append(housemate("Sven",0))
housemates.append(housemate("House",0))

refreshList()



housemates[10].setBeerCount(12)

refreshBeerList()

housemates.append(housemate("AARON",1))

refreshList()




try:
    GPIO.add_event_detect(17, GPIO.FALLING, callback=pinDetect, bouncetime=40)
except:
    print("not currently running on a RPI 2")

window.mainloop()