#!/usr/bin/env python

# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier verions
# are not fast enough!

from __future__ import division
from threading import Thread
from model.reading import Reading
import time
import RPi.GPIO as GPIO
import queue
import logging

logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

DEBUG = 0
GPIO.setmode(GPIO.BCM)

class SensorReader(Thread):
    RCpin = 0
    threshold = 0.0
    maxLength = 3
    readingLimit = 15000
    readings = [readingLimit] * maxLength
    readingsSum = readingLimit * maxLength
    readingIdx = 0
    isBlinking = False

    def __init__(self, pin, threshold, name):
        super(SensorReader, self).__init__(name = name)
        logging.debug("Sensor constructor called")
        self.RCpin = pin
        self.threshold = threshold

    def saveReading(self, reading):
        # remove old reading from array 
        self.readingsSum -= self.readings[self.readingIdx]
        # overwrite old reading with new
        self.readings[self.readingIdx] = reading
        # add new reading to sum
        self.readingsSum += self.readings[self.readingIdx]        

        if (self.readingIdx == self.maxLength - 1):
            # reset index if reached max
            self.readingIdx = 0
        else:
            # increase index by one
            self.readingIdx += 1

    def readSensor(self):
        reading = 0
        GPIO.setup(self.RCpin, GPIO.OUT)
        GPIO.output(self.RCpin, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(self.RCpin, GPIO.IN)
        # This takes about 1 millisecond per loop cycle
        while (GPIO.input(self.RCpin) == GPIO.LOW and reading < self.readingLimit):
                reading += 1
        return reading         

    def run(self):
        logging.debug("Starting readings")
        while True:
            reading = self.readSensor()
            avgReading = (self.readingsSum / self.maxLength)
            readingRatio = avgReading / reading
            # logging.debug("New reading: %d, avgReading = %.2f, readingRatio = %.2f" %(reading, avgReading, readingRatio))
            if (readingRatio > self.threshold):
                if (not self.isBlinking):
                    logging.debug("Blink!")
                    readingItem = Reading(reading, readingRatio)
                    queue.put(readingItem)
                    self.isBlinking = True
            else:
                self.isBlinking = False
                self.saveReading(reading)

     
