import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN)
counter = 0
def pinDetect(pin):
    global counter
    counter += 1
    print("pin pushed")
    print("counter: " + str(counter))
 
def loop():
  try:
    raw_input()
  # Wanneer er op CTRL+C gedrukt wordt.
  except KeyboardInterrupt:  
    # GPIO netjes afsluiten
    GPIO.cleanup() 
 
# Zet de GPIO pin als ingang.

# Gebruik een interrupt, wanneer actief run subroutinne 'gedrukt'
GPIO.add_event_detect(17, GPIO.RISING, callback=pinDetect, bouncetime=20)
 
loop()