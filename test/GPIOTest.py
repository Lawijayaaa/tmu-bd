import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
dataNum = 1

while True:
    print("data no : " + str(dataNum))
    print(GPIO.input(13))
    print(GPIO.input(17))
    print(GPIO.input(22))
    print(GPIO.input(27))
    print("~~~")
    dataNum = dataNum + 1
    time.sleep(2)