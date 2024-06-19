#from pymodbus.client import ModbusSerialClient
"""from time import sleep
import mysql.connector"""

#client = ModbusSerialClient(method='rtu', port='/dev/ttyACM0', baudrate=9600)

"""db = mysql.connector.connect(
    host = "localhost",
    user = "client",
    passwd = "raspi",
    database= "iot_trafo_client")"""

class parameter:
    def __init__(self, name, highAlarm, lowAlarm, highTrip, lowTrip, status):
        self.name = name
        self.highAlarm = highAlarm
        self.lowAlarm = lowAlarm
        self.highTrip = highTrip
        self.lowTrip = lowTrip
        self.status = status

dataSet = [parameter(None, None, None, None, None, None)]*52

print(dataSet)

"""
while True:
    getTemp = client.read_holding_registers(4, 3, slave = 1)
    getElect1 = client.read_holding_registers(0, 29, slave = 2)
    getElect2 = client.read_holding_registers(46, 5, slave = 2)
    getElect3 = client.read_holding_registers(800, 6, slave = 2)
    getHarmV = client.read_holding_registers(806, 90, slave = 2)
    getHarmA = client.read_holding_registers(896, 90, slave = 2)
"""