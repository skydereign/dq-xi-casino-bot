import screen_positions as pos
import glob
import cv2
import re


def convert(card):
    conversion = {'j':11, 'q':12, 'k':13, 'a':1}
    if card == 'joker':
        return (-1, 'W')
    elif card == 'back':
        return None
    elif card[1:] in conversion:
        return (conversion[card[1:]], card[0])
    else:
        return (int(card[1:]), card[0])

def least_diff(img, compare_dict):
    img_channels = cv2.split(img)
    max_diff = 10000
    card_name = None

    for compare_img in compare_dict:
        running_diff = 0
        compare_channels = cv2.split(compare_dict[compare_img])

        # run through the r/g/b channels
        for i in range(0, len(compare_channels)):
            running_diff += cv2.absdiff(img_channels[i], compare_channels[i]).mean()

        if running_diff < max_diff:
            max_diff = running_diff
            card_name = compare_img


    return convert(card_name)


def get(img):
    cards = []

    for i in range(0, pos.get_num('cards')):
        card_img = pos.get(img, 'cards', i) # img[pos[1]:pos[1]+dim[1], pos[0]:pos[0]+dim[0]]
        cards.append(least_diff(card_img, _cards))

    return cards


def load_all():
    filenames = glob.glob('cards/*png')

    for filename in filenames:
        _cards[filename[:-4].split('/')[-1]] = cv2.imread(filename)


_cards = {}
load_all()

if __name__ == '__main__':
    # run tests
    tests = glob.glob('card_shots/*png')
    name_regex = re.compile(r'.*/(.*).png')


    for filename in tests:
        name = name_regex.match(filename).group(1)
        card_names = name.split('_')
        card_names = [convert(card) for card in card_names]

        screen = cv2.imread(filename)
        hand = get(screen)
        if hand != card_names:
            print 'hand not the same', hand, card_names

