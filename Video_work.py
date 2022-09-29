import cv2
import subprocess
import sys
import time

video_file = open("video_timing.txt","w")
video_file.write("20")
video_file.close()
time.sleep(1)
Video_rec = subprocess.Popen([sys.executable, 'Video.py'])
#time.sleep(5)
print(Video_rec)
for i in range(1000):
    print("kek")