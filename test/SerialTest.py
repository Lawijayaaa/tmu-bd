#!/usr/bin/env python3
from pymodbus.client import ModbusSerialClient
import time

#init modbus device
client = ModbusSerialClient(method='rtu', port='/dev/ttyACM0', baudrate=9600)
loop = False

def testBatch():
    getTemp = client.read_holding_registers(0, 10, slave = 1)
    getElect = client.read_holding_registers(0, 29, slave = 2)
    writeRly = client.write_coil(4, False, slave = 3)
    print(getTemp.registers)
    print(getElect.registers)
    print(writeRly)
    print("~~~")

#Loop
if loop:
    while True:
        testBatch()
        time.sleep(2)
else:   
    testBatch()
