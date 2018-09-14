import screen_positions as pos
from PIL import Image
import glob
import cv2
import re


DISP = True


def wait():
    key = cv2.waitKey()
            
    if key == 27 or key == ord('q'):
        exit()

        
def show(img, name="frame", wait_after=False):
    if DISP:
        cv2.imshow(name, img)

        if wait_after:
            wait()






screens = glob.glob('card_shots/*png')

name_regex = re.compile(r'.*/(.*).png')

cards = {}

for filename in screens:
    name = name_regex.match(filename).group(1)
    card_names = name.split('_')

    screen = cv2.imread(filename)

    for i in range(0, len(card_names)):
        # position = positions[i]
        card_name = card_names[i]
        
        # right = position[0] + dimensions[0]
        # bottom = position[1] + dimensions[1]
        card_img = pos.get(screen, 'cards', i) # screen[position[1]:bottom, position[0]:right]

        # only store it once
        if card_name not in cards:
            cards[card_name] = card_img


# export cards
for card in cards:
    cv2.imwrite('cards/' + card + '.png', cards[card])
