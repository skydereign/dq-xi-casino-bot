import screen_positions as pos
import detect_win_type
import numpy as np
import read_tokens
import traceback
import read_hand
import logging
import jokers
import state
import glob
import time
import cv2
import sys
import mss
import re


PAYOUT_THRESHOLD = 3000
expected_next_state = None
base_value_of_hand = 0
value_of_hand = 0
round_num = 0
prev_hand = None
starting = 176255
total_money = starting
multiplier = 0 # 1 if blue, 10 if red
captured_item = False

def press_button(button):
    print("press " + button)
    sys.stdout.flush()
    time.sleep(0.4)


# get the index to store items
item_count = -1
for filename in glob.glob('items/*png'):
    item_count = max(int(re.match(r'items\\(.*).png', filename).group(1)), item_count)

item_count += 1


def log_hand(frame):
    hand = read_hand.get(frame)
    logging.info('cards,{}'.format(hand))
    # may want to parse differences

    return hand

def start(color, frame, prev_state):
    global total_money, multiplier, captured_item

    # reset
    captured_item = False

    if color == 'red':
        multiplier = 10
    else:
        multiplier = 1

    current_money = read_tokens.get(frame)

    if current_money:
        total_money = current_money
        print(total_money)

    total_money -= 100 * multiplier
    logging.info('pay {},{}'.format(100 * multiplier, total_money))
    logging.info('reset hand')
    press_button('x')
    return ['hand_dealt']

def won_hand(frame, prev_state):
    global base_value_of_hand, value_of_hand, round_num, multiplier
    win_type = detect_win_type.get(frame, multiplier)
    log_hand(frame)

    if win_type:
        base_value_of_hand = win_type[1]
        value_of_hand = win_type[1]
        logging.info('won hand,{}'.format(win_type))

    round_num = 0
    press_button('x')
    press_button('wait')
    press_button('x')
    return ['double_prompt']

def hand_dealt(frame, prev_state):
    # process hand
    hand = log_hand(frame)
    keep = jokers.get_should_keep(hand)

    logging.info('keeping,{}'.format(keep))

    # check if there are cards to keep
    if True in keep:
        for i in range(0, len(keep)):
            if True not in keep[i:]:
                # escape if done
                break

            card = keep[i]

            if card:
                press_button('x')
                press_button('right')
            else:
                press_button('right')

    press_button('down')
    press_button('x')
    return ['won_hand', 'loss']

def loss(frame, prev_state):
    # possibly new cards, store hand
    log_hand(frame)
    press_button('wait')
    press_button('x')
    return ['start_red', 'start_blue']

def double_prompt(frame, prev_state):
    global round_num, value_of_hand, total_money, base_value_of_hand, multiplier

    round_num += 1

    # require 3 rounds, but if it is over threshold after quit, otherwise wait for five rounds
    if base_value_of_hand == 100 * multiplier:
        if round_num > 10:
            total_money += value_of_hand
            logging.info('won,{},{}'.format(value_of_hand, total_money))
            press_button('o')
            return ['win']
    elif value_of_hand >= 10000 * multiplier or round_num > 5:
        total_money += value_of_hand
        logging.info('won,{},{}'.format(value_of_hand, total_money))
        press_button('o')
        return ['win']

    if prev_state != 'won_han':
        print('double value_of_hand', value_of_hand)
        value_of_hand *= 2

    press_button('x')
    return ['double', 'treasure']

def treasure(frame, prev_state):
    press_button('wait')
    press_button('x')
    return ['double']

def double(frame, prev_state):
    # don't have a state for double_select, for now always picks the first card
    press_button('x')
    print('wait')
    press_button('x')

    return ['double_end_with_treasure', 'double_win', 'tie', 'loss']

def double_win(frame, prev_state):
    log_hand(frame)
    press_button('x')
    return ['treasure_unlock', 'double_prompt']

def treasure_unlock(frame, prev_state):
    press_button('x')
    return ['double_prompt']

def win(frame, prev_state):
    press_button('x')
    return ['play_again', 'double_end_with_treasure']

def tie(frame, prev_state):
    # store hand
    log_hand(frame)
    hand = read_hand.get(frame)
    press_button('x')

    return ['double']

def double_end_with_treasure(frame, prev_state):
    log_hand(frame)
    press_button('wait')
    press_button('x')
    return ['obtain_item', 'treasure_trove']

def obtain_item(frame, prev_state):
    global item_count, captured_item
    # store the item
    if not captured_item:
        captured_item = True
        cv2.imwrite('items/{}.png'.format(item_count), pos.get(frame, 'dialog_box'))
        item_count += 1

    press_button('wait')
    press_button('x')

    return ['play_again']

def treasure_trove(frame, prev_state):
    global item_count
    cv2.imwrite('items/{}.png'.format(item_count), pos.get(frame, 'dialog_box'))
    item_count += 1

    press_button('x')
    return ["play_again"]

def play_again(frame, prev_state):
    press_button('x')
    return ['start_red', 'start_blue']

def run():
    crashes = 0
    logging.basicConfig(filename='output.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info('start---------------------------------------------------------------------------')
    state.transitions['start_red'] = lambda frame, prev_state: start('red', frame, prev_state)
    state.transitions['start_blue'] = lambda frame, prev_state: start('blue', frame, prev_state)
    state.transitions['hand_dealt'] = hand_dealt
    state.transitions['loss'] = loss
    state.transitions['won_hand'] = won_hand
    state.transitions['win'] = win
    state.transitions['double_prompt'] = double_prompt
    state.transitions['treasure'] = treasure
    state.transitions['double'] = double
    state.transitions['double_win'] = double_win
    state.transitions['treasure_unlock'] = treasure_unlock
    state.transitions['tie'] = tie
    state.transitions['double_end_with_treasure'] = double_end_with_treasure
    state.transitions['obtain_item'] = obtain_item
    state.transitions['play_again'] = play_again
    state.transitions['treasure_trove'] = treasure_trove

    # get the part of the screen to track    
    monitor = {'top': 0, 'left': -1920, 'width': 1920, 'height':1080 }

    with mss.mss() as sct:
        # Part of the screen to capture
        window_anchor = cv2.imread('misc/ps4_window_anchor.png', cv2.IMREAD_UNCHANGED)
        frame = np.array(sct.grab(monitor))

        res = cv2.matchTemplate(frame, window_anchor, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        monitor['top'] = top_left[1]
        monitor['left'] = top_left[0] - 1920
        monitor['width'] = 995
        monitor['height'] = 593

    stopped = 0

    while crashes < 3:
        try:
            frame = np.array(sct.grab(monitor))

            small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            cv2.imshow('frame', small)

            new_state = state.get(frame)
            state.enter(state.get(frame), frame)

            # if it gets stuck, press x
            if new_state == None:
                stopped += 1

                if stopped > 5:
                    press_button('x')
            else:
                stopped = 0

            key = cv2.waitKey(2000)
            if key == 27 or key == ord('q'):
                cv2.destroyAllWindows()
                break
            
            crashes = 0

        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
            crashes += 1

    logging.info('close---------------------------------------------------------------------------')


run()
print('closed')