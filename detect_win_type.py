import screen_positions as pos
import cv2


yes = cv2.imread('misc/yes_hand.png')
no = cv2.imread('misc/no_hand.png')

win_types = [
    ['royal_jelly_flush', 50000],
    ['royal_flush', 10000],
    ['five_kind', 5000],
    ['straight_flush', 2000],
    ['four_kind', 1000],
    ['full_house', 500],
    ['flush', 400],
    ['straight', 300],
    ['three_kind', 100],
    ['two_kind', 100]
]

def get(img):
    num_win_types = pos.get_num('got_hands')

    for i in range(0, num_win_types):
        hand_region = pos.get(img, 'got_hands', i)
        yes_diff = cv2.absdiff(hand_region, yes).mean()
        no_diff = cv2.absdiff(hand_region, no).mean()

        if yes_diff < 80 and no_diff > 80:
            return win_types[i]

    return None

if __name__ == '__main__':
    import glob

    for filename in glob.glob('state_base/got_hand*'):
        print(filename)
        img = cv2.imread(filename)
        print(get(img), '\n')


    
