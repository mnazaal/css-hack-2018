import smbus
import RPi.GPIO as GPIO
import math
import time
import numpy as np
import os


GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.IN)

THRESHOLD = 0.0007679
#power management registers, on, off, sleep, etc.

PWR_MGMT_1 = 0x6B
PWR_MGMT_2 = 0x6C

# I2C stuff
MPU6050_ADDRESS_DEFAULT= 0x68

# register map, both high, low but change to low implemented in readWord
MPU6050_RA_ACCEL_XOUT_H = 0x3B
MPU6050_RA_ACCEL_XOUT_L = 0x3C
MPU6050_RA_ACCEL_YOUT_H = 0x3D
MPU6050_RA_ACCEL_YOUT_L = 0x3E
MPU6050_RA_ACCEL_ZOUT_H = 0x3F
MPU6050_RA_ACCEL_ZOUT_L =0x40

MPU6050_RA_ACCEL_CONFIG = 0x1C

def readWord(adr):
    highRange = bus.read_byte_data(MPU6050_ADDRESS_DEFAULT, adr)
    lowRange = bus.read_byte_data(MPU6050_ADDRESS_DEFAULT, adr+1)
    value = (highRange << 8 ) + lowRange
    return value

def readWord2C(adr):
    value = readWord(adr)
    if (value >= 0x8000):
        return -((65535 - value)+1)
    else:
        return value

def changeAccelRange(param):
    bus.write_byte_data(MPU6050_ADDRESS_DEFAULT, MPU6050_RA_ACCEL_CONFIG, param)
    return

#set up bus object
bus = smbus.SMBus(1)

#wake up IMU
bus.write_byte_data(MPU6050_ADDRESS_DEFAULT, PWR_MGMT_1, 0)

#set up full 16g range
changeAccelRange(3)

#read scaled accel data
try:
	while(True):
		accel_xout_scaled = readWord2C(MPU6050_RA_ACCEL_XOUT_H)/2048.0
		accel_yout_scaled = readWord2C(MPU6050_RA_ACCEL_YOUT_H)/2048.0
		accel_zout_scaled = readWord2C(MPU6050_RA_ACCEL_ZOUT_H)/2048.0
		accel = np.array([accel_xout_scaled, accel_yout_scaled, accel_zout_scaled])
		accelmod = np.inner(np.multiply(0.001,accel),np.multiply(accel, 0.001))
		if (accelmod>THRESHOLD):
			print(accelmod)
			GPIO.output(16, GPIO.HIGH)
			os.system("sudo python RadioCommsv2.py")
			while(not GPIO.input(18)):
				time.sleep(10)
			GPIO.output(16, GPIO.LOW)
except: 
	print("oh dear some kind of error occured :(")

finally:
	GPIO.cleanup()
