#from pymodbus.client import ModbusSerialClient
from time import sleep
import mysql.connector

#client = ModbusSerialClient(method='rtu', port='/dev/ttyACM0', baudrate=9600)

db = mysql.connector.connect(
    host = "localhost",
    user = "client",
    passwd = "raspi",
    database= "iot_trafo_client")

"""
while True:
    getTemp = client.read_holding_registers(4, 3, slave = 1)
    getElect1 = client.read_holding_registers(0, 29, slave = 2)
    getElect2 = client.read_holding_registers(46, 5, slave = 2)
    getElect3 = client.read_holding_registers(800, 6, slave = 2)
    getHarmV = client.read_holding_registers(806, 90, slave = 2)
    getHarmA = client.read_holding_registers(896, 90, slave = 2)
"""
cursor3 = db.cursor()
sql3 = "SELECT * FROM transformer_settings"
cursor3.execute(sql3)
trafoSetting = cursor3.fetchall()[0]
print(len(trafoSetting))O