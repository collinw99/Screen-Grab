import numpy as np
import cv2
from mss import mss
from pynput.mouse import Listener

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
            return False

with Listener(on_click=on_click) as listener:
    listener.join()

# ==========================================================

while True:
    sct_img = sct.grab(bounding_box)
    cv2.imshow('screen', np.array(sct_img))

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
