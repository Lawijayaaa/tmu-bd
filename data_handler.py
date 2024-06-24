#from pymodbus.client import ModbusSerialClient
from pymodbus.client import ModbusSerialClient
from toolboxTMU import parameter, initParameter, dataParser
import mysql.connector
import time

client = ModbusSerialClient(method='rtu', port='/dev/ttyACM0', baudrate=9600)

db = mysql.connector.connect(
    host = "localhost",
    user = "client",
    passwd = "raspi",
    database= "iot_trafo_client")

def main():
    dataLen = 56
    watchedData = 29
    CTratio = 100
    PTratio = 2

    inputData = [0]*dataLen
    currentStat = [0]*watchedData
    currentTrip = [0]*watchedData
    dataSet = [parameter("Name", 0, False, None, None, None, None, 3, 0)]
    for i in range(0, dataLen-1):
        dataSet.append(parameter("Name", 0, False, None, None, None, None, 3, 0))
    
    cursor = db.cursor()
    sqlTrafoSetting = "SELECT * FROM transformer_settings"
    sqlTrafoData = "SELECT * FROM transformer_data"
    sqlTrafoStatus = "SELECT * FROM transformer_status"
    sqlTripStatus = "SELECT * FROM trip_status"
    sqlTripSetting = "SELECT * FROM trip_settings"
    sqlDIscan = "SELECT * FROM di_scan"
    sqlDOscan = "SELECT * FROM do_scan"
    sqlUpdateTrafoStat = "UPDATE transformer_data SET status = %s WHERE trafoId = 1"
    sqlUpdateTransformerStatus = """UPDATE transformer_status SET 
                Vab = %s , Vbc = %s , Vca = %s ,
                Current1 = %s , Current2 = %s , Current3 = %s , Ineutral = %s ,
                THDVoltage1 = %s, THDVoltage2 = %s , THDVoltage3 = %s , 
                THDCurrent1 = %s, THDCurrent2 = %s , THDCurrent3 = %s ,                
                PF = %s , Freq = %s , BusTemp1 = %s , BusTemp2 = %s , BusTemp3 = %s ,
                OilTemp = %s , WTITemp1 = %s , WTITemp2 = %s , WTITemp3 = %s ,
                Pressure = %s , OilLevel = %s , H2ppm = %s , Moistureppm = %s ,
                Uab = %s , Ubc = %s , Uca = %s WHERE trafoId = 1"""
    sqlUpdateTripStatus = """UPDATE trip_status SET 
                Vab = %s , Vbc = %s , Vca = %s ,
                Current1 = %s , Current2 = %s , Current3 = %s , Ineutral = %s ,
                THDVoltage1 = %s, THDVoltage2 = %s , THDVoltage3 = %s , 
                THDCurrent1 = %s, THDCurrent2 = %s , THDCurrent3 = %s ,                
                PF = %s , Freq = %s , BusTemp1 = %s , BusTemp2 = %s , BusTemp3 = %s ,
                OilTemp = %s , WTITemp1 = %s , WTITemp2 = %s , WTITemp3 = %s ,
                Pressure = %s , OilLevel = %s , H2ppm = %s , Moistureppm = %s ,
                Uab = %s , Ubc = %s , Uca = %s WHERE trafoId = 1"""

    while True:
        start_time = time.time()
        cursor.execute(sqlTrafoSetting)
        trafoSetting = cursor.fetchall()[0]
        cursor.execute(sqlTrafoData)
        trafoData = cursor.fetchall()[0]
        cursor.execute(sqlTripSetting)
        tripSetting = cursor.fetchall()[0]
        cursor.execute(sqlDIscan)
        inputIO = cursor.fetchall()
        cursor.execute(sqlDOscan)
        outputIO = cursor.fetchall()
        cursor.execute(sqlTrafoStatus)
        prevStat = list(cursor.fetchall()[0][1:])
        cursor.execute(sqlTripStatus)
        prevTrip = list(cursor.fetchall()[0][1:])
        db.commit()
        
        for i in range(3, 5):
            if outputIO[i][2] == 1:
                client.write_coil(i, True, slave = 3)
            elif outputIO[i][2] == 0:
                client.write_coil(i, False, slave = 3)
        
        #Process 1 gather all data
        getTemp = client.read_holding_registers(4, 3, slave = 1)
        getElect1 = client.read_holding_registers(0, 29, slave = 2)
        getElect2 = client.read_holding_registers(46, 5, slave = 2)
        getElect3 = client.read_holding_registers(800, 6, slave = 2)
        getHarmV = client.read_holding_registers(806, 90, slave = 2)
        getHarmA = client.read_holding_registers(896, 90, slave = 2)
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
        inputData = dataParser(getTemp, getElect1, getElect2, getElect3, getH2, getMoist, dataLen, CTratio, PTratio)
        inputData[39] = inputIO[6][2] #Oil Temp
        inputData[43] = inputIO[7][2] #Pressure
        inputData[44] = oilStat
        dataResult = initParameter(dataSet, inputData, trafoSetting, trafoData, tripSetting, dataLen) 
        
        #Process 2 Updating data relay and db
        #define trafoStat based on new data
        maxStat = 0
        i = 0
        for data in dataResult:
            if data.isWatched:
                maxStat = data.trafoStat if data.trafoStat > maxStat else maxStat
                currentStat[i] = data.status
                currentTrip[i] = data.trafoStat
                #print(data.name)
                i = i + 1
        print(currentTrip)
        print(prevTrip)
        if prevStat != currentStat or prevTrip != currentTrip:
            print("lhoo")
            #update transformer Status db
            cursor.execute(sqlUpdateTransformerStatus, currentStat)
            cursor.execute(sqlUpdateTripStatus, currentTrip)
            #update db trafoStat
            cursor.execute(sqlUpdateTrafoStat, (maxStat,))
            db.commit()    
            #actuating trafoStat
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