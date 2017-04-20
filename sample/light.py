#this is a test
#import the GPIO and time package
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 4
GPIO.setup(led, GPIO.OUT)
# loop through 50 times, on/off for 1 second
for i in range(10):
    GPIO.output(led,True)
    time.sleep(1)
    GPIO.output(led,False)
    time.sleep(1)
GPIO.cleanup()
