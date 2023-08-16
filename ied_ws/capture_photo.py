#!urs/bin/python3
import os
import subprocess
from datetime import datetime

def capture_photo():
	timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

	base_filename = "photo_"
	filename = f"{base_filename}{timestamp}.jpg"
	raspistill_cmd = f"raspistill -o {filename} -t 2000"
	subprocess.run(raspistill_cmd, shell=True)

if __name__ =="__main__":
	capture_photo()
