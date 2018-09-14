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

def start(frame, prev_state):
    print('press x')
    return ['hand_dealt']


def won_hand(frame, prev_state):
    global base_value_of_hand, value_of_hand
    win_type = detect_win_type.get(frame)

    if win_type:
        base_value_of_hand = win_type[1]
        value_of_hand = win_type[1]

    print('press x')
    return ['double']

def hand_dealt(frame, prev_state):
    hand = read_hand.get(frame)
    keep = jokers.get_should_keep(hand)
    print(hand)
    print(keep)

    for card in keep:
        if card:
            print('press x')
            print('press right')
            print('wait 0.3')
        else:
            print('press right')

    print('press down')
    print('press x')
    return ['won_hand', 'loss']

def loss(frame, prev_state):
    print('press x')
    return ['start']

def double_prompt(frame, prev_state):
    global round_num, value_of_hand

    round_num += 1

    if prev_state != 'won_han':
        print('double value_of_hand', value_of_hand)
        value_of_hand *= 2

    if value_of_hand > PAYOUT_THRESHOLD:
        print('press o')
        return ['win']

    print('press x')
    return ['double', 'treasure']

def treasure(frame, prev_state):
    print('press x')
    return ['double']

def double(frame, prev_state):
    # don't have a state for double_select, for now always picks the first card
    print('press x')
    print('wait 0.3')
    print('press x')

    return ['double_end_with_treasure', 'double_win', 'tie', 'loss']

def double_win(frame, prev_state):
    print('press x')
    return ['treasure_unlock', 'double_prompt']

def treasure_unlock(frame, prev_state):
    print('press x')
    return ['double_prompt']

def win(frame, prev_state):
    print('press x')
    return ['play_again', 'double_end_with_treasure']

def tie(frame, prev_state):
    # store hand
    hand = read_hand.get(frame)
    
    return ['double']

def double_end_with_treasure(frame, prev_state):
    print('press x')
    return ['obtain_item']

def obtain_item(frame, prev_state):
    print('press x')
    return ['play_again']

def play_again(frame, prev_state):
    print('press x')
    return ['start']

if __name__ == '__main__':
    state.transitions['start'] = start
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
        
    frame = cv2.imread('state_base/got_hand_full_house.png')
    state.enter(state.get(frame), frame)

    frame = cv2.imread('state_base/double_prompt.png')
    state.enter(state.get(frame), frame)

