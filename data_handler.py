#from pymodbus.client import ModbusSerialClient
from pymodbus.client import ModbusSerialClient
from toolboxTMU import parameter, sqlLibrary, initParameter, dataParser, harmonicParser
import mysql.connector, time, datetime, math

def main():
    dataLen = 56
    watchedData = 29
    CTratio = 1200
    PTratio = 2
    eddyLosesGroup = 0.02
    designedKrated = 1
    loadCoef = 5
    cycleTime = 2 / 60
    
    client = ModbusSerialClient(method='rtu', port='/dev/ttyACM0', baudrate=9600)
    db = mysql.connector.connect(
        host = "localhost",
        user = "client",
        passwd = "raspi",
        database= "iot_trafo_client")
    cursor = db.cursor()
    
    inputData = [0]*dataLen
    currentStat = [0]*watchedData
    currentTrip = [0]*watchedData
    dataName = ['']*watchedData
    activeParam = [None]*watchedData
    activeFailure = [None]*watchedData
    kRated = [0, 0, 0]
    deRating = [0, 0, 0]
    hSquared = [0]*32
    timePassed = [0]*3
    deltaHi1 = [0]*3
    deltaHi2 = [0]*3
    deltaH1 = [0]*3
    deltaH2 = [0]*3
    lastLoadDefiner = [0]*3
    currentLoadDefiner = [0]*3
    raisingLoadBool = [True, True, True]
    loadFactor = [0]*3
    dataSet = [parameter("Name", 0, False, None, None, None, None, 3, 0)]
    for i in range(0, dataLen-1):
        dataSet.append(parameter("Name", 0, False, None, None, None, None, 3, 0))
    messageReason = ['Extreme Low',
                'Low', 
                'Back Normal', 
                'High', 
                'Extreme High']
    msgEvent = [None] * watchedData
    msgReminder = [None] * watchedData
    previousTime = excelPrevTime = datetime.datetime.now()
    cursor.execute(sqlLibrary.sqlFailure)
    listFailure = cursor.fetchall()
    for i in range(0, len(listFailure)):
        if listFailure[i][2] == None:
            activeFailure[activeFailure.index(None)] = listFailure[i]
    print(activeFailure)
    
    while True:
        start_time = time.time()
        cursor.execute(sqlLibrary.sqlTrafoSetting)
        trafoSetting = cursor.fetchall()[0]
        cursor.execute(sqlLibrary.sqlTrafoData)
        trafoData = cursor.fetchall()[0]
        cursor.execute(sqlLibrary.sqlTripSetting)
        tripSetting = cursor.fetchall()[0]
        cursor.execute(sqlLibrary.sqlDIscan)
        inputIO = cursor.fetchall()
        cursor.execute(sqlLibrary.sqlDOscan)
        outputIO = cursor.fetchall()
        cursor.execute(sqlLibrary.sqlConstantWTI, (str(trafoData[27]), ))
        constantWTI = cursor.fetchall()[0]
        cursor.execute(sqlLibrary.sqlTrafoStatus)
        prevStat = list(cursor.fetchall()[0][1:])
        cursor.execute(sqlLibrary.sqlTripStatus)
        prevTrip = list(cursor.fetchall()[0][1:])
        db.commit()
        CTratio = trafoData[26]

        if len(activeFailure):
            for i in range(0, len(activeFailure)):
                if activeFailure[i]:
                    activeParam[i] = activeFailure[i][4]

        for i in range(3, 5):
            if outputIO[i][2] == 1:
                client.write_coil(i, True, slave = 3)
            elif outputIO[i][2] == 0:
                client.write_coil(i, False, slave = 3)

        getTemp = client.read_holding_registers(4, 3, slave = 1)
        getElect1 = client.read_holding_registers(0, 29, slave = 2)
        getElect2 = client.read_holding_registers(46, 5, slave = 2)
        getElect3 = client.read_holding_registers(800, 6, slave = 2)
        getHarmV = client.read_holding_registers(806, 90, slave = 2)
        getHarmI = client.read_holding_registers(896, 90, slave = 2)
        #getH2 = client.read_holding_registers(896, 90, slave = 2)
        getH2 = 0
        #getMoist = client.read_holding_registers(896, 90, slave = 2)
        getMoist = 0
        oilLevelAlarm = inputIO[4][2]
        oilLevelTrip = inputIO[5][2]        
        if (oilLevelAlarm and oilLevelTrip) or oilLevelTrip:
            oilStat = 1
        elif oilLevelAlarm:
            oilStat = 2
        elif oilLevelAlarm == 0 and oilLevelTrip == 0:
            oilStat = 3
        inputHarmonicV = harmonicParser(getHarmV)
        inputHarmonicI = harmonicParser(getHarmI)
        cursor.execute(sqlLibrary.sqlUpdateVHarm1, inputHarmonicV[0])
        cursor.execute(sqlLibrary.sqlUpdateVHarm2, inputHarmonicV[1])
        cursor.execute(sqlLibrary.sqlUpdateVHarm3, inputHarmonicV[2])
        cursor.execute(sqlLibrary.sqlUpdateIHarm1, inputHarmonicI[0])
        cursor.execute(sqlLibrary.sqlUpdateIHarm2, inputHarmonicI[1])
        cursor.execute(sqlLibrary.sqlUpdateIHarm3, inputHarmonicI[2])
        inputData = dataParser(getTemp, getElect1, getElect2, getElect3, getH2, getMoist, dataLen, CTratio, PTratio)
        inputData[39] = inputIO[6][2] #Oil Temp
        inputData[43] = inputIO[7][2] #Pressure
        inputData[44] = oilStat
        #test parameter
        inputData[4] = 430
        inputData[32] = 1
        inputData[53] = inputData[55] = 0
        inputData[14] = 5

        for i in range(0, 3): loadFactor[i] = (inputData[i + 6])/trafoData[6]
        for i in range(0, 3):
            currentLoadDefiner[i] = inputData[i + 6]
            if currentLoadDefiner[i] - lastLoadDefiner[i] >= loadCoef:
                timePassed[i] = 1
                deltaHi1[i] = deltaH1[i]
                deltaHi2[i] = deltaH2[i]
                raisingLoadBool[i] = True
                lastLoadDefiner[i] = currentLoadDefiner[i]
            elif lastLoadDefiner[i] - currentLoadDefiner[i] >= loadCoef:
                timePassed[i] = 1
                deltaHi1[i] = deltaH1[i]
                deltaHi2[i] = deltaH2[i]
                raisingLoadBool[i] = False
                lastLoadDefiner[i] = currentLoadDefiner[i]
            else:
                timePassed[i] = timePassed[i] + 1
            try:
                if raisingLoadBool[i]:
                    deltaH1[i] = deltaHi1[i] + (((constantWTI[1] * trafoData[25] * trafoData[21]) * (math.pow(loadFactor[i], constantWTI[0])) - deltaHi1[i]) * (1 - math.exp((-1 * cycleTime * timePassed[i])/(constantWTI[2] * constantWTI[4]))))
                    deltaH2[i] = deltaHi2[i] + ((((constantWTI[1] - 1) * trafoData[25] * trafoData[21]) * (math.pow(loadFactor[i], constantWTI[0])) - deltaHi2[i]) * (1 - math.exp((-1 * cycleTime * timePassed[i] * constantWTI[2])/constantWTI[3])))
                    #print("rumus beban naik")
                else:
                    deltaH1[i] = constantWTI[1] * trafoData[25] * trafoData[21] * math.pow(loadFactor[i], constantWTI[0]) + (deltaHi1[i] - (constantWTI[1] * trafoData[25] * trafoData[21] * math.pow(loadFactor[i], constantWTI[0]))) * (math.exp((-1 * cycleTime * timePassed[i])/(constantWTI[2] * constantWTI[4])))
                    deltaH2[i] = (constantWTI[1] - 1) * trafoData[25] * trafoData[21] * math.pow(loadFactor[i], constantWTI[0]) + (deltaHi2[i] - (constantWTI[1] - 1) * trafoData[25] * trafoData[21] * math.pow(loadFactor[i], constantWTI[0])) * math.exp(((-1 * cycleTime * timePassed[i] * constantWTI[4])/constantWTI[3]))
                    #print("rumus beban turun")
            except:
                pass
            inputData[i + 40] = (round((inputData[39] + (deltaH1[i] - deltaH2[i])) * 100))/100

        kRatedlist = inputHarmonicI
        for i in range(0, 32):
            hSquared[i] = math.pow(((2*(i+1))-1), 2)
        for i in range(0, len(inputHarmonicI)):
            for j in range(0, len(inputHarmonicI[i])):
                kRatedlist[i][j] = math.pow((inputHarmonicI[i][j])/100, 2) * hSquared[j]
            kRated[i] = round(sum(kRatedlist[i]))
            deRating[i] = 100 * (math.pow((eddyLosesGroup + 1)/(kRated[i]*eddyLosesGroup + 1), 0.8) - math.pow((eddyLosesGroup + 1)/(designedKrated*eddyLosesGroup + 1), 0.8) + 1)
            if deRating[i] > 100:
                deRating[i] = 100
            inputData[i*2 + 45] = kRated[i]
            inputData[i*2 + 46] = (round(deRating[i] * 100))/100

        dataResult = initParameter(dataSet, inputData, trafoSetting, trafoData, tripSetting, dataLen) 
        sendData = [datetime.datetime.now()] + inputData
        cursor.execute(sqlLibrary.sqlInsertData, sendData)
        db.commit()
        
        maxStat = 0
        i =  0
        for data in dataResult:
            if data.isWatched:
                maxStat = data.trafoStat if data.trafoStat > maxStat else maxStat
                currentStat[i] = data.status
                currentTrip[i] = data.trafoStat
                dataName[i] = data.name
                #print(data.name)
                if data.status != prevStat[i]:
                    if data.status != 3:
                        if data.name in activeParam:
                            lastTimestamp = activeFailure[activeParam.index(data.name)][1]
                            duration = int((datetime.datetime.now() - lastTimestamp).total_seconds())
                            errorVal = [duration, activeFailure[activeParam.index(data.name)][0]]
                            cursor.execute(sqlLibrary.sqlResolveFailure, errorVal)
                            activeFailure[activeParam.index(data.name)] = None
                            activeParam[activeParam.index(data.name)] = None
                        errorVal = [datetime.datetime.now(), messageReason[data.status - 1], data.name, str(data.value)]
                        cursor.execute(sqlLibrary.sqlInsertFailure, errorVal)
                        cursor.execute(sqlLibrary.sqlLastFailure)
                        lastActive = cursor.fetchall()[0]
                        activeFailure[activeFailure.index(None)] = lastActive
                        loadProfile = str((round((data.value / trafoData[6]) * 10000))/100) + " Percent , Rated Current = " + str(trafoData[6])
                        msgEvent[i] = str(data.name + " " + messageReason[data.status - 1] + " , Value = " + (loadProfile if i == 3 or i == 4 or i == 5 else str(data.value)) + "\n" + "Time Occurence : " + str(datetime.datetime.now()))
                    elif data.status == 3:
                        lastTimestamp = activeFailure[activeParam.index(data.name)][1]
                        duration = int((datetime.datetime.now() - lastTimestamp).total_seconds())
                        errorVal = [duration, activeFailure[activeParam.index(data.name)][0]]
                        cursor.execute(sqlLibrary.sqlResolveFailure, errorVal)
                        activeFailure[activeParam.index(data.name)] = None
                        activeParam[activeParam.index(data.name)] = None
                        msgEvent[i] = None
                i = i + 1
        
        if prevStat != currentStat or prevTrip != currentTrip:
            print("Send Telegram Lhooo")
            tele = list(filter(None, msgEvent))
            if tele:
                for message in tele:
                    print(message)
            else:
                pass
            cursor.execute(sqlLibrary.sqlUpdateTransformerStatus, currentStat)
            cursor.execute(sqlLibrary.sqlUpdateTripStatus, currentTrip)
            cursor.execute(sqlLibrary.sqlUpdateTrafoStat, (maxStat,))
            db.commit()
            if maxStat == 1:
                client.write_coil(0, True, slave = 3)
                client.write_coil(1, False, slave = 3)
                client.write_coil(2, False, slave = 3)
            elif maxStat == 2:
                client.write_coil(0, True, slave = 3)
                client.write_coil(1, True, slave = 3)
                client.write_coil(2, False, slave = 3)
            elif maxStat == 3:
                client.write_coil(0, True, slave = 3)
                client.write_coil(1, False, slave = 3)
                client.write_coil(2, True, slave = 3)
            else:
                client.write_coil(0, False, slave = 3)
                client.write_coil(1, False, slave = 3)
                client.write_coil(2, False, slave = 3)
        else:
            #print("okejek")
            pass
        
        if int((datetime.datetime.now() - previousTime).total_seconds()) > 30:
            print("sekadar mengingatkan")
            for i in range(0, len(activeFailure)):
                if activeFailure[i]:
                    failureIndex = dataName.index(activeFailure[i][4])
                    msgReminder[failureIndex] = str(activeFailure[i][4] + " " + activeFailure[i][3] + " , Value = " + activeFailure[i][5] + "\n" + "Time Occurence : " + str(activeFailure[i][1]))                    
                    print(msgReminder[failureIndex])
            previousTime = datetime.datetime.now()
        #time.sleep(3.9)
        #for data in dataResult:
        #    print(vars(data))
        
        cycleTime = time.time() - start_time
        print("Loop time >> %s seconds" % cycleTime)
        #break
        
if __name__ == "__main__":
    main()