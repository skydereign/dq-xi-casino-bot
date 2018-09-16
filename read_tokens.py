import screen_positions as pos
from PIL import Image
import numpy as np
import pytesseract
import cv2

def get(frame):
    roi = pos.get(frame, 'tokens')
    roi = cv2.resize(roi, (0, 0), fx=3, fy=3)

    output = cv2.inRange(roi, (0, 0, 0), (150, 150, 150))
    return pytesseract.image_to_string(Image.fromarray(output))


if __name__ == '__main__':
    frame = cv2.imread('state_base/start.png')
    
    print get(frame)
