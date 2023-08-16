#!/usr/bin/python3

import cv2
import tflite_runtime.interpreter as tflite
import numpy as np
import time
import picamera

interpreter = tflite.Interpreter("/home/pi/ied_ws/my_model2.tflite")
print("model lodaded")

interpreter.allocate_tensors()

print(cv2.__version__)

camera = picamera.PiCamera()
camera.resolution = (96,64)
camera.framerate=5
#camera.exposure_mode = 'off'
camera.shutter_speed = 2000
#camera.awb_mode = 'off'

time.sleep(2)

labels = ["trash", "recycle", "empty"]


#with picamera.array.PiRGBArray(camera) as stream:
#	for frame in camera.capture_continuout(stream, format="bgr", use_video_port=True):
x = 1
while x==1:
	#x = 0
	#stream.truncate(0)
	image = np.empty((camera.resolution[1], camera.resolution[0], 3), dtype=np.uint8)
	camera.capture(image, "bgr", use_video_port=True)
	#camera.close()

	image2 = cv2.resize(image,(50,50))
	arr = np.array([np.float32(np.asarray(image2) / 255.0)])

	input_details = interpreter.get_input_details()
	output_details = interpreter.get_output_details()


	interpreter.set_tensor(input_details[0]['index'], arr)
	interpreter.invoke()
	output_data = interpreter.get_tensor(output_details[0]['index'])

	print(labels[np.argmax(output_data)])
	print(output_data)

	big = cv2.resize(image2, (500,500))
	cv2.imshow("image", big)

	#camera = picamera.PiCamera()
	#camera.resolution = (96,64)
	#camera.framerate = 5
	cv2.waitKey(1000)

