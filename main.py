#!/usr/bin/env python

import RPi.GPIO as GPIO
import logging
from worker import Worker
from sensor_reader import SensorReader
import sys

logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

try:
    worker1 = Worker("worker1")
    worker2 = Worker("worker2")
    worker1.daemon = True
    worker2.daemon = True
    
    logging.info("starting worker1")
    worker1.start()

    logging.info("starting worker2")
    worker2.start()

    reader = SensorReader(27, 1.25, "reader")
    reader.daemon = True
    reader.start()

    reader.join()
except KeyboardInterrupt:
    logging.debug("Shutdown requested...exiting")
    # GPIO.cleanup()
    sys.exit(0)