#!/usr/bin/python
import RPi.GPIO as GPIO
import time

print("hi")

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)
time.sleep(1)
GPIO.output(17, GPIO.LOW)


GPIO.cleanup()


print("bye")



