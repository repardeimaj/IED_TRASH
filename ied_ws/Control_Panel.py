#!/usr/bin/python
#time.sleep(1)
import RPi.GPIO as GPIO
import time

print("Start")

#Initalization
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)
GPIO.output(17, GPIO.HIGH)

GPIO.setup(5, GPIO.IN)
GPIO.setup(6, GPIO.OUT)
GPIO.output(6, GPIO.LOW)

GPIO.setup(19, GPIO.IN)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, GPIO.LOW)

GPIO.setup(9, GPIO.IN)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.LOW)

GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.LOW)

TF = True

#Looping till button push
while TF == True:
	if GPIO.input(5) == 1:
		GPIO.output(6, GPIO.HIGH)
		print("Green")
		TF = False 
		
while TF == False:
	if GPIO.input(19) == 1:
		GPIO.output(26, GPIO.HIGH)
		GPIO.output(6, GPIO.LOW)
		print("RED")
		TF = True 
		
while TF == True:
	if GPIO.input(9) == 1:
		GPIO.output(11, GPIO.HIGH)
		GPIO.output(26, GPIO.LOW)
		print("Yellow")
		TF = False 
		
while TF == False:
	if GPIO.input(27) == 1:
		GPIO.output(22, GPIO.HIGH)
		GPIO.output(11, GPIO.LOW)
		print("White")
		time.sleep(1)
		TF = True 

#Turn off the 3.3V from GPIO 17
GPIO.output(22, GPIO.LOW)
GPIO.output(17, GPIO.LOW)

GPIO.cleanup()

print("Done")
