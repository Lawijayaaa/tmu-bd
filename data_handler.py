#from pymodbus.client import ModbusSerialClient
from pymodbus.client import ModbusSerialClient
from toolboxTMU import parameter, initParameter
import mysql.connector
import time

client = ModbusSerialClient(method='rtu', port='/dev/ttyACM0', baudrate=9600)

db = mysql.connector.connect(
    host = "localhost",
    user = "client",
    passwd = "raspi",
    database= "iot_trafo_client")

getTemp = client.read_holding_registers(4, 3, slave = 1)
getElect1 = client.read_holding_registers(0, 29, slave = 2)
getElect2 = client.read_holding_registers(46, 5, slave = 2)
getElect3 = client.read_holding_registers(800, 6, slave = 2)
getHarmV = client.read_holding_registers(806, 90, slave = 2)
getHarmA = client.read_holding_registers(896, 90, slave = 2)

print(getTemp)
print(getElect1)
print(getElect2)
print(getElect3)
print(getHarmV)
print(getHarmA)

start_time = time.time()
cursorTrafoSetting = db.cursor()
sqlTrafoSetting = "SELECT * FROM transformer_settings"
cursorTrafoSetting.execute(sqlTrafoSetting)
trafoSetting = cursorTrafoSetting.fetchall()[0]

cursorTrafoData = db.cursor()
sqlTrafoData = "SELECT * FROM transformer_data"
cursorTrafoData.execute(sqlTrafoData)
trafoData = cursorTrafoData.fetchall()[0]

cursorTripSetting = db.cursor()
sqlTripSetting = "SELECT * FROM trip_settings"
cursorTripSetting.execute(sqlTripSetting)
tripSetting = cursorTripSetting.fetchall()[0]

dataLen = 56

inputData = [0]*dataLen

dataSet = [parameter(None, None, False, None, None, None, None, None, None)]
for i in range(0, dataLen-1):
    dataSet.append(parameter(None, None, False, None, None, None, None, None, None))

dataResult = initParameter(dataSet, inputData, trafoSetting, trafoData, tripSetting, dataLen)

for data in dataResult:
    data = data.toJson()
    #print(data)

print("Loop time >> %s seconds" % (time.time() - start_time))
