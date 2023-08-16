#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import cv2
import tflite_runtime.interpreter as tflite
import numpy as np
import time
import RPi.GPIO as GPIO
from collections import Counter
import threading

GPIO.setmode(GPIO.BCM)

#Conveyor Pins
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

#Sorting door pins
GPIO.setup(25, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(1, GPIO.OUT)

#Landing platform pins
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

#LED Pins
GPIO.setup(15, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)

#Button pins
#Green is 2 and Red is 3
GPIO.setup(2, GPIO.IN)
GPIO.setup(3, GPIO.IN)
stop = True

conveyor_pins = [12,16,20,21]
landing_pins = [6,13,19,26]
sorting_pins = [25,8,7,1]

interpreter = tflite.Interpreter("/home/pi/ied_ws/my_model7.tflite")
print("model lodaded")

interpreter.allocate_tensors()

state = 0

print(cv2.__version__)

cap = cv2.VideoCapture("/dev/video0",cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_EXPOSURE, 20)
time.sleep(5)

labels = ["trash", "recycle", "empty"]

predictions = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]

print("start")

sequence = [[1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,1,0], [0,0,1,1], [1,0,0,1]]

def step(degrees, direction, pins):
	steps = (int)(degrees * 512 / 360)

	for i in range(steps):
		if direction:
			sequence2 = sequence
		else:
			sequence2 = sequence[::-1]

		for step in sequence2:
			GPIO.output(pins[0], step[0])
			GPIO.output(pins[1], step[1])
			GPIO.output(pins[2], step[2])
			GPIO.output(pins[3], step[3])
			time.sleep(0.002)

def identify():
	while(True):
		global state
		print("identify start")
		for i in range(1):
				success, image = cap.read()
				image2 = cv2.resize(image, (50,50))

				arr = np.array([np.float32(np.asarray(image2) / 255.0)])

				input_details = interpreter.get_input_details()
				output_details = interpreter.get_output_details()
				interpreter.set_tensor(input_details[0]['index'], arr)
				interpreter.invoke()
				output_data = interpreter.get_tensor(output_details[0]['index'])



				if (np.argmax(output_data) != state):
					state = np.argmax(output_data)
					#print(labels[state])
					#print(output_data)

				big = cv2.resize(image2, (500,500))
				cv2.imshow("image", image)
				cv2.waitKey(1)

				predictions.pop(0)
				predictions.append(state)
				counter = Counter(predictions)
				most_common = counter.most_common(1)[0][0]
				state = most_common

				if state == 1:
					GPIO.output(15, GPIO.LOW)
					GPIO.output(14, GPIO.HIGH)
				elif state == 0:
					GPIO.output(15, GPIO.HIGH)
					GPIO.output(14, GPIO.LOW)
				else:
					GPIO.output(15, GPIO.LOW)
					GPIO.output(14, GPIO.LOW)
				print(labels[state])
		

def button():
	global stop
	while(True):
#Green
		if GPIO.input(2) == GPIO.LOW:
			stop = False
#Red
		elif GPIO.input(3) == GPIO.LOW:
			stop = True
		time.sleep(0.1)

thread2 = threading.Thread(target=button)
thread = threading.Thread(target=identify)
thread.start()
thread2.start()

print("dkdlklakdj")

while(True):
	
	print(stop)
	if stop == False:
		print("OK this is a test")
	#Checks to see if something is in the ID box
		#identify()
	#if not emtpy then
		if state != 2:
			if state == 0:
				step(120,False,landing_pins)#True is covering the hole, 90 degrees angle
				time.sleep(2)
				step(120,True,landing_pins)
				time.sleep(0.5)
			else: 
				step(75,False,sorting_pins) #True is reset, False is set, 65 degree angle
				step(120,False,landing_pins)
				time.sleep(2)
				step(75,True,sorting_pins) 
				step(120,True,landing_pins)
				time.sleep(0.5)

	#if emtpy then move the converybelt
		else:
			step(90,True,conveyor_pins)#True is , 180 degree steps till notice item 
			time.sleep(0.1)

#step(65, False, sorting_pins)
#step(5080, True, conveyor_pins)
step(90, False, landing_pins)
time.sleep(0.2)
step(90, True, landing_pins)

GPIO.cleanup()
