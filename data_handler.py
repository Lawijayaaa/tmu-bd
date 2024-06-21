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
    CTratio = 100
    PTratio = 2

    inputData = [0]*dataLen
    dataSet = [parameter("Name", 0, False, None, None, None, None, 3, 0)]
    for i in range(0, dataLen-1):
        dataSet.append(parameter("Name", 0, False, None, None, None, None, 3, 0))

    while True:
        start_time = time.time()

        cursor = db.cursor()
        sql = "SELECT * FROM transformer_settings"
        cursor.execute(sql)
        trafoSetting = cursor.fetchall()[0]
        sql = "SELECT * FROM transformer_data"
        cursor.execute(sql)
        trafoData = cursor.fetchall()[0]
        sql = "SELECT * FROM trip_settings"
        cursor.execute(sql)
        tripSetting = cursor.fetchall()[0]
        sql = "SELECT number, name, state FROM di_scan"
        cursor.execute(sql)
        inputIO = cursor.fetchall()[0]
        sql = "SELECT number, name, state FROM do_scan"
        cursor.execute(sql)
        outputIO = cursor.fetchall()[0]
        db.commit()

        print(outputIO)
        print(inputIO)

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
        
        inputData = dataParser(getTemp, getElect1, getElect2, getElect3, getH2, getMoist, dataLen, CTratio, PTratio)

        
        
        dataResult = initParameter(dataSet, inputData, trafoSetting, trafoData, tripSetting, dataLen)
        time.sleep(3.9)
        
        """
        for data in dataResult:
            print(vars(data))
        """
        print("Loop time >> %s seconds" % (time.time() - start_time))
        break

if __name__ == "__main__":
    main()