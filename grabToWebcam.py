#!/usr/bin/python
import os
import numpy as np
import cv2
from mss import mss
from pynput.mouse import Listener
from PIL import Image
import time
import pyfakewebcam

device_num = 6
bounding_box = {'top': 100, 'left': 0, 'width': 400, 'height': 300}
click_count = 0
sct = mss()

print("Click mouse to choose screen capture corners...")

# mouse click logic =======================================

def on_click(x, y, button, pressed):
    global click_count, bounding_box
    if (pressed):
        if (click_count == 0):
            print("Top left corner: ({0},{1})".format(x,y))
            click_count += 1
            bounding_box["left"] = x
            bounding_box["top"] = y
        elif (click_count == 1):
            print("Bottom right corner: ({0},{1})".format(x,y))
            bounding_box["width"] = x-bounding_box["left"]
            bounding_box["height"] = y-bounding_box["top"]
            print("Size: {0}x{1}".format(bounding_box["width"], bounding_box["height"]))
            return False

with Listener(on_click=on_click) as listener:
    listener.join()

# ==========================================================

# webcam logic =============================================
os.system('sudo rmmod --force v4l2loopback')
os.system('sudo modprobe v4l2loopback video_nr={0} exclusive_caps=1 card_label="CamWow"'.format(device_num))

camera = pyfakewebcam.FakeWebcam('/dev/video{0}'.format(device_num+1), bounding_box["width"], bounding_box["height"])

print("Writing capture to webcam device...")
while True:
    sct_img = sct.grab(bounding_box)
    sct_rgb = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    img_arr_rgb = np.array(sct_rgb, dtype=np.uint8)
    camera.schedule_frame(img_arr_rgb)

# ==========================================================