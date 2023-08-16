#!/usr/bin/python3

import cv2
import tflite_runtime.interpreter as tflite
import numpy as np
import time
import RPi.GPIO as GPIO
from collections import Counter

GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)


interpreter = tflite.Interpreter("/home/pi/ied_ws/my_model5.tflite")
print("model lodaded")

interpreter.allocate_tensors()

state = 0

print(cv2.__version__)

cap = cv2.VideoCapture("/dev/video0",cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_EXPOSURE, 20)
time.sleep(5)


labels = ["trash", "recycle", "empty"]

predictions = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]

while(True):
	success, image = cap.read()
	image2 = cv2.resize(image[60:], (50,50))

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
	cv2.imshow("image", image[60:])
	cv2.waitKey(1)

	predictions.pop(0)
	predictions.append(state)
	counter = Counter(predictions)
	most_common = counter.most_common(1)[0][0]

	if most_common == 1:
		GPIO.output(15, GPIO.HIGH)
		GPIO.output(14, GPIO.LOW)
	elif most_common == 0:
		GPIO.output(15, GPIO.LOW)
		GPIO.output(14, GPIO.HIGH)
	else:
		GPIO.output(15, GPIO.LOW)
		GPIO.output(14, GPIO.LOW)
	print(labels[most_common])
