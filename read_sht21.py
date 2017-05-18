#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Importing libraries
import time
import rpi_i2c
import os
import sys


# Creating the class sht21
class sht21:

    i2c = rpi_i2c.I2C()                                       # I2C Wrapper Class (recall the class)

# Complete measurement function
    def measure(self, dev=1, scl=3, sda=2):
        self.open(dev, scl, sda)                              # Open the device
        t = self.read_temperature()                           # Get temperature
        rh = self.read_humidity()                             # Get humidity
        self.i2c.close()                                      # Close the device
        return (t, rh)

# Open and initialise the I2C port in the raspberry
    def open(self, dev=1, scl=3, sda=2):
        self.i2c.open(0x40,dev, scl, sda)                     # Open the port of the device and set the the clock and data wire
        self.i2c.write([0xFE])                                # Execute Softreset Command  (default T=14Bit RH=12)
        time.sleep(0.050)

# Temperature measurement function
    def read_temperature(self):
        self.i2c.write([0xF3])                                # Trigger T measurement (no hold master)
        time.sleep(0.066)                                     # Waiting time, typ=66ms, max=85ms @ 14Bit resolution
        data = self.i2c.read(3)
        if (self._check_crc(data, 2)):
            t = ((data[0] << 8) + data[1]) & 0xFFFC           # Set status bits to zero
            t = -46.82 + ((t * 175.72) / 65536)               # T = 46.82 + (175.72 * ST/2^16 )
            return round(t, 1)
        else:
            return None

# Humidity measurement function
    def read_humidity(self):
        self.i2c.write([0xF5])                                # Trigger RH measurement (no hold master)
        time.sleep(0.25)                                      # Waiting time, typ=22ms, max=29ms @ 12Bit resolution
        data = self.i2c.read(3)
        if (self._check_crc(data, 2)):
            rh = ((data[0] << 8) + data[1]) & 0xFFFC          # Set status bits to zero
            rh = -6 + ((125 * rh) / 65536)
            if (rh > 100): rh = 100
            return round(rh, 1)
        else:
            return None

# Close function (closes the i2c connection)
    def close(self):
        self.i2c.close()

# Checksum function (standar function in order to know when some error appear)
    def _check_crc(self, data, length):
        
        #Calculates checksum for n bytes of data and compares it with expected
        crc = 0
        for i in range(length):
            crc ^= (ord(chr(data[i])))
            for bit in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x131                   # CRC POLYNOMIAL
                else:
                    crc = (crc << 1)
        return True if (crc == data[length]) else False

# Taking data
if __name__ == "__main__":
  SHT21 = sht21()
  gpio_number = [17, 22, 27]
  gpio_index = 0
  sensor_number = ["sensor_1", "sensor_3", "sensor_2"]
  sensor_index = 0

  for index, value in enumerate(gpio_number):
    gpio_file = open("/sys/class/gpio/gpio" + str(value) + "/value", 'w')
    if index == 0:
      gpio_file.write("1") 
    else:
      gpio_file.write("0") 
    gpio_file.close() 

  while True:
    print "Measure SHT21, Gpio", gpio_number[gpio_index] 
    (t0, rh0) = SHT21.measure(None,3,2)  # Use GPIOs SCL=3, SDA=2
    if(t0==None or rh0==None or t0 > 50 or rh0 > 100):
        print("Error: Value is None")
	#continue
	print "Skipping Gpio Pin: " + str(gpio_number[gpio_index]) + "\n"
	gpio_file = open("/sys/class/gpio/gpio" + str(gpio_number[gpio_index]) + "/value", "w")
	gpio_file.write("0")
	gpio_file.close()
	gpio_index += 1	
	if gpio_index == len(gpio_number):
	  gpio_index = 0
	sensor_index += 1
	if sensor_index == len(sensor_number):
	  sensor_index = 0
	print "sleeping..." + "\n"
	time.sleep(3)
	gpio_file = open("/sys/class/gpio/gpio" + str(gpio_number[gpio_index]) + "/value", "w")
	gpio_file.write("1")
	gpio_file.close()
        continue	
		
    current_time = time.strftime("%d/%m/%Y %H:%M:%S")
    print (current_time, "Temperature: ", t0 ,"   Humidity: ", rh0)
    myrow = str(current_time) + ',' + str(t0) + ',' + str(rh0) + '\n'
    
    # writing values in csv file
    print ("Saving csv for ", str(sensor_number[sensor_index]), "  " , str(gpio_number[gpio_index]))
    fd = open(str(sensor_number[sensor_index]) + "," + str(gpio_number[gpio_index]) + ".csv",'a')
    fd.write(myrow)
    fd.close()
    sensor_index += 1
    if sensor_index == len(gpio_number):
	sensor_index = 0

    #print "global index", gpio_index
    for index, value in enumerate(gpio_number):
        gpio_file = open("/sys/class/gpio/gpio" + str(value) + "/value", 'r')
        #print gpio_file.read()[0]
        if gpio_file.read()[0] == '1':
            #print "Open gpio", value
    	    gpio_file.close()
            gpio_file = open("/sys/class/gpio/gpio" + str(value) + "/value", 'w')
	    gpio_file.write("0") 
    	    gpio_file.close()
            # increase global index
            gpio_index += 1
            if gpio_index == len(gpio_number):
                print "Reached the end of gpio list.."
                gpio_index = 0
            # write 
	    gpio_file = open("/sys/class/gpio/gpio" + str(gpio_number[gpio_index]) + "/value", 'w')
	    gpio_file.write("1") 
    	    gpio_file.close() 
	    break
        else:
    	    gpio_file.close() 


    print "sleep...\n"
    time.sleep(3)	
