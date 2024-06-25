#from pymodbus.client import ModbusSerialClient
from pymodbus.client import ModbusSerialClient
from toolboxTMU import parameter, sqlLibrary, initParameter, dataParser, harmonicParser
import mysql.connector, time, datetime

def main():
    dataLen = 56
    watchedData = 29
    CTratio = 100
    PTratio = 2
    
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
    dataSet = [parameter("Name", 0, False, None, None, None, None, 3, 0)]
    for i in range(0, dataLen-1):
        dataSet.append(parameter("Name", 0, False, None, None, None, None, 3, 0))

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
        cursor.execute(sqlLibrary.sqlTrafoStatus)
        prevStat = list(cursor.fetchall()[0][1:])
        cursor.execute(sqlLibrary.sqlTripStatus)
        prevTrip = list(cursor.fetchall()[0][1:])
        db.commit()
        
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
                #print(data.name)
                i = i + 1
        
        if prevStat != currentStat or prevTrip != currentTrip:
            print("lhoo")
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
            print("okejek")
        
        #time.sleep(3.9)
        #for data in dataResult:
        #    print(vars(data))
        print("Loop time >> %s seconds" % (time.time() - start_time))
        #break
        
if __name__ == "__main__":
    main()