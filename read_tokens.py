import screen_positions as pos
from PIL import Image
import numpy as np
import pytesseract
import cv2

def get(frame):
    roi = pos.get(frame, 'tokens')
    roi = cv2.resize(roi, (0, 0), fx=3, fy=3)

    lower = (0, 0, 0, 0) if frame.shape[2] == 4 else (0, 0, 0)
    upper = (150, 150, 150, 255) if frame.shape[2] == 4 else (150, 150, 150)

    output = cv2.inRange(roi, lower, upper)
    value = pytesseract.image_to_string(Image.fromarray(output))
    try:
        return int(value)
    except:
        return None


if __name__ == '__main__':
    frame = cv2.imread('state_base/start.png')
    
    print(get(frame))
