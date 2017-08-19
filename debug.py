#!/usr/bin/env python

import RPi.GPIO as GPIO, time, os
 
DEBUG = 0
GPIO.setmode(GPIO.BCM)
 
def RCtime (RCpin):
        reading = 0
        GPIO.setup(RCpin, GPIO.OUT)
        GPIO.output(RCpin, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(RCpin, GPIO.IN)
        while (GPIO.input(RCpin) == GPIO.LOW and reading <= 15000):
                reading += 1
        return reading
 
while True:
        print RCtime(27)

