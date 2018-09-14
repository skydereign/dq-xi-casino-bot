import detect_win_type
import read_hand
import jokers
import logging
import state
import cv2

PAYOUT_THRESHOLD = 1500
expected_next_state = None
base_value_of_hand = 0
value_of_hand = 0
round_num = 0

def press_x(frame, prev_state):
    print 'press x'

def store_and_continue(frame, prev_state):
    hand = read_hand.get(frame)
    print 'press x'
    
def down_x(frame, prev_state):
    print 'press down'
    print 'wait 0.3'
    print 'press x'

def won_hand(frame, prev_state):
    global base_value_of_hand, value_of_hand
    win_type = detect_win_type.get(frame)

    if win_type:
        base_value_of_hand = win_type[1]
        value_of_hand = win_type[1]

    print 'press x'
    return ['double']
    
def hand_dealt(frame, prev_state):
    hand = read_hand.get(frame)
    keep = jokers.get_should_keep(hand)
    print hand
    print keep
    
    for card in keep:
        if card:
            print 'press x'
            print 'press right'
            print 'wait 0.3'
        else:
            print 'press right'

    print 'press down'
    print 'press x'
    return ['won_hand', 'loss']

def double_prompt(frame, prev_state):
    global round_num, value_of_hand
    
    round_num += 1

    if prev_state != 'won_han':
        print 'double value_of_hand', value_of_hand
        value_of_hand *= 2

    if value_of_hand > PAYOUT_THRESHOLD:
        print 'press o'
        return ['win']

    print 'press x'
    return ['double', 'treasure']

    
    
if __name__ == '__main__':
    state.transitions['start'] = press_x
    state.transitions['hand_dealt'] = hand_dealt
    state.transitions['loss'] = press_x
    state.transitions['won_hand'] = won_hand
    state.transitions['double_prompt'] = double_prompt

    
    frame = cv2.imread('state_base/got_hand_full_house.png')    
    state.enter(state.get(frame), frame)
    
    frame = cv2.imread('state_base/double_prompt.png')
    state.enter(state.get(frame), frame)

