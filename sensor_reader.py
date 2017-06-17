#!/usr/bin/env python

# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier verions
# are not fast enough!

from threading import Thread
import time
import datetime
import os
import RPi.GPIO as GPIO
from Queue import Queue


DEBUG = 1
GPIO.setmode(GPIO.BCM)
queue = Queue(10)

class SensorReader(Thread):
    def __init__(self, pin, threshold):
        super(SensorReader, self).__init__()
        print "Sensor constructor called"
        self.RCpin = pin
        self.readings = [0,0,0,0,0]
        self.readingsSum = 0
        self.readingIdx = 0
        self.threshold = threshold
        self.maxLength = 5
        self.readingsLength = 0
        self.lightState = "dark"

    def saveReading(self, reading):
        # remove old reading from array, if avaiable 
        if (self.readingsLength != 0):
            self.readingsSum -= self.readings[self.readingIdx]
        # overwrite old reading with new
        self.readings[self.readingIdx] = reading
        # add new reading to sum
        self.readingsSum += self.readings[self.readingIdx]
        
        # count up length (if not reached maxLength)
        if (self.readingsLength < self.maxLength):
            self.readingsLength += 1

        if (self.readingIdx == self.maxLength - 1):
            # reset index if reached max
            self.readingIdx = 0
        else:
            # increase index by one
            self.readingIdx += 1

    def run(self):
        print "Starting readings"
        global queue
        
        while True:
            reading = self.readSensor()
            print "New reading: " + str(reading)
            if (self.readingsLength != 0):
                avgReading = (self.readingsSum / self.readingsLength)
                newReadingRatio = avgReading / reading
                if (newReadingRatio > self.threshold):
                    if (self.lightState != "light"):
                        print "BLINK!!!!"
                        queue.put("blink")
                        self.lightState = "light"
                else:
                    self.lightState = "dark"
                print "avgReading = " + str(avgReading) + " newReadingRatio = %.2f" % (newReadingRatio)
            else:
                print "array is empty"
            print "array: " + str(self.readings)
            self.saveReading(reading)

    def readSensor(self):
        reading = 0
        GPIO.setup(self.RCpin, GPIO.OUT)
        GPIO.output(self.RCpin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.setup(self.RCpin, GPIO.IN)
        # This takes about 1 millisecond per loop cycle
        while (GPIO.input(self.RCpin) == GPIO.LOW and reading < 15000):
                reading += 1
        return reading
try:
    reader = SensorReader(27, 1.25)
    reader.daemon = True
    reader.start()
    while True:
        item = queue.get()
        if (item is not None):
            print "something was put in the queue: " + item
            f = open("registered_blinks.csv", "a+")
            utcTime = str(datetime.datetime.utcnow().isoformat())
            f.write("blink, %s\n" %(utcTime))
            f.close()
        time.sleep(5)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
