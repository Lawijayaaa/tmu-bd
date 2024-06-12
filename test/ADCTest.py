import Adafruit_ADS1x15
from time import sleep
# Initialize the ADC.
adc = Adafruit_ADS1x15.ADS1115(address = 0x48, busnum = 1)

while True:
    val = adc.read_adc(0, gain = 2)
    print(val)
    sleep(1)

"""
##################################
# 0-10V Voltage Input
##################################
# Read the ADC.
# Param 1 = Analog Input Channel (0-3).
# Param 2 = ADC Gain (Gain 1 for 0-10V, Gain 2 for 0-5V or 0-20mA).
val = adc.read_adc(0, gain=1)

# Calculate the analog voltage (V).
# Full scale value = 32767
# Full scale voltage = 4.096V
# Voltage divider scale = 2.5
# voltage(V) = val / 32767 * 4.096 * 2.5
voltage = val / 3200


##################################
# 0-5V Voltage Input
##################################
# Read the ADC.
# Param 1 = Analog Input Channel (0-3).
# Param 2 = ADC Gain (Gain 1 for 0-10V, Gain 2 for 0-5V or 0-20mA).
val = adc.read_adc(0, gain=2)

# Calculate the analog voltage (V).
# Full scale value = 32767
# Full scale voltage = 2.048V
# Voltage divider scale = 2.5
# voltage(V) = val / 32767 * 2.048 * 2.5
voltage = val / 6400


##################################
# 0-20mA Current Input
# (DIP Switch must be ON)
##################################
# Read the ADC.
# Param 1 = Analog Input Channel (0-3).
# Param 2 = ADC Gain (Gain 1 for 0-10V, Gain 2 for 0-5V or 0-20mA).
val = adc.read_adc(0, gain=2)

# Calculate the current.
# Full scale value = 32767
# Full scale voltage = 2.048V
# Voltage divider scale = 2.5
# Shunt resistor value = 250 ohm
# voltage(V) = val / 32767 * 2.048 * 2.5
# current(mA) = voltage * 1000 / 250
voltage = val / 1600
"""