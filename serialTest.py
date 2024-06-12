#!/usr/bin/env python3
from pymodbus.client import ModbusSerialClient
import RPi.GPIO as GPIO
import time

#init modbus device, db, gps
client = ModbusSerialClient(method='rtu', port='/dev/ttyACM0', baudrate=9600)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)

#Loop

while True:
    #getTemp = client.read_holding_registers(0, 10, slave = 1)
    #getElect = client.read_holding_registers(0, 29, slave = 2)
    #writeRly = client.write_coil(0, False, slave = 3)
    #print(getTemp.registers)
    #print(getElect.registers)
    #print(writeRly)
    print(GPIO.input(13))
    print(GPIO.input(17))
    print(GPIO.input(22))
    print(GPIO.input(27))
    print("~~~")
    time.sleep(2)

    
getTemp = client.read_holding_registers(0, 10, slave = 1)
getElect = client.read_holding_registers(0, 29, slave = 2)
writeRly = client.write_coil(0, False, slave = 3)
print(getTemp.registers)
print(getElect.registers)
print(writeRly)
