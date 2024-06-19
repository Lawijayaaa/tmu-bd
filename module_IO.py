from toolboxTMU import TimerEx
from time import sleep
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import mysql.connector
import json

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
adc = Adafruit_ADS1x15.ADS1115(address = 0x48, busnum = 1)

valveStat = 0
gasEnabler = True
openValveDuration = 10

db = mysql.connector.connect(
    host = "localhost",
    user = "client",
    passwd = "raspi",
    database = "iot_trafo_client")

def gasRelease():
    global valveStat
    valveStat = 0

def updateJson(name, val):
    with open("module_IO.json", "r") as jsonFile: data = json.load(jsonFile)
    data[name] = val
    with open("module_IO.json", "w") as jsonFile: json.dump(data, jsonFile)

def main():
    #start_time = time.time()
    global valveStat
    timer = TimerEx(interval_sec = openValveDuration, function = gasRelease)
    with open("module_IO.json", "r") as jsonFile: data = json.load(jsonFile)
    resetBuzz = data["resetBuzz"]
    prevStatBuzz = data["prevStatBuzz"]
    cursorReadStat = db.cursor()
    sqlReadStat = "SELECT * FROM transformer_data"
    cursorUpdateDO = db.cursor()
    sqlUpdateDO = "UPDATE do_scan SET state = %s WHERE number = %s"
    cursorUpdateDI = db.cursor()
    sqlUpdateDI = "UPDATE di_scan SET state = %s WHERE number = %s"
    #print("Set up time >> %s seconds" % (time.time() - start_time))
    while True:
        #start_time = time.time()
        oilLevelAlarm = 1 if adc.read_adc(1, gain = 2) > 25000 else 0
        oilLevelTrip = 1 if adc.read_adc(0, gain = 2) > 25000 else 0
        if (oilLevelAlarm and oilLevelTrip) or oilLevelTrip:
            oilStat = 1
        elif oilLevelAlarm:
            oilStat = 2
        elif oilLevelAlarm == 0 and oilLevelTrip == 0:
            oilStat = 3
        if gasEnabler:
            with open("module_IO.json", "r") as jsonFile: data = json.load(jsonFile)
            resetValve = data["resetValve"]
            prevStatOil = data["prevStatOil"]
            if timer.is_alive() == False and resetValve == False:
                if oilStat < prevStatOil:
                    timer.start()
                    valveStat = 1
                    updateJson("resetValve", True)
                else:
                    updateJson("prevStatOil", oilStat)
            elif timer.is_alive() or resetValve:
                if oilStat >= prevStatOil:
                    timer.cancel()
                    valveStat = 0
                    updateJson("resetValve", False)
                elif valveStat == 0:
                    updateJson("prevStatOil", oilStat)
        pbStat = GPIO.input(13)
        analogIn1 = 0 if adc.read_adc(3, gain = 2) < 0 else adc.read_adc(3, gain = 2)
        analogIn2 = 0 if adc.read_adc(2, gain = 2) < 0 else adc.read_adc(2, gain = 2)
        cursorUpdateDI.execute(sqlUpdateDI, [pbStat, 0])
        cursorUpdateDI.execute(sqlUpdateDI, [GPIO.input(17), 1])
        cursorUpdateDI.execute(sqlUpdateDI, [GPIO.input(22), 2])
        cursorUpdateDI.execute(sqlUpdateDI, [GPIO.input(27), 3])
        cursorUpdateDI.execute(sqlUpdateDI, [oilLevelAlarm, 4])
        cursorUpdateDI.execute(sqlUpdateDI, [oilLevelTrip, 5])
        cursorUpdateDI.execute(sqlUpdateDI, [analogIn1, 6])
        cursorUpdateDI.execute(sqlUpdateDI, [analogIn2, 7])
        cursorReadStat.execute(sqlReadStat)
        trafoStat = cursorReadStat.fetchall()[0][28]
        db.commit()
        if trafoStat == 1:
            cursorUpdateDO.execute(sqlUpdateDO, [1, 0])
            cursorUpdateDO.execute(sqlUpdateDO, [0, 1])
            cursorUpdateDO.execute(sqlUpdateDO, [0, 2])
        elif trafoStat == 2:
            cursorUpdateDO.execute(sqlUpdateDO, [0, 0])
            cursorUpdateDO.execute(sqlUpdateDO, [1, 1])
            cursorUpdateDO.execute(sqlUpdateDO, [0, 2])
        elif trafoStat == 3:
            cursorUpdateDO.execute(sqlUpdateDO, [0, 0])
            cursorUpdateDO.execute(sqlUpdateDO, [0, 1])
            cursorUpdateDO.execute(sqlUpdateDO, [1, 2])
        else:
            cursorUpdateDO.execute(sqlUpdateDO, [0, 0])
            cursorUpdateDO.execute(sqlUpdateDO, [0, 1])
            cursorUpdateDO.execute(sqlUpdateDO, [0, 2])
        cursorUpdateDO.execute(sqlUpdateDO, [valveStat, 4])
        db.commit()
        if trafoStat != prevStatBuzz and trafoStat != 0:
            if resetBuzz:
                #print("buzzer off")
                cursorUpdateDO.execute(sqlUpdateDO, [0, 3])
                prevStatBuzz = trafoStat
                updateJson("prevStatBuzz", trafoStat)
            else:
                #print("buzzer on")
                cursorUpdateDO.execute(sqlUpdateDO, [1, 3])
        else:
            #print("buzzer off")
            cursorUpdateDO.execute(sqlUpdateDO, [0, 3])
            prevStatBuzz = trafoStat
            updateJson("prevStatBuzz", trafoStat)
            resetBuzz = False
        db.commit()
        if resetBuzz:
            resetBuzz = True
        else:
            if pbStat:
                resetBuzz = True
            else:
                resetBuzz = False
        updateJson("resetBuzz", resetBuzz)
        #print(valveStat)
        sleep(0.25)
        #print("Loop time >> %s seconds" % (time.time() - start_time))
    
if __name__ == "__main__":
    main()