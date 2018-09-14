import screen_positions as pos
import logging
import cv2

states = [
    'start',
    'hand_dealt',
    'loss',
    'double_prompt',
    'treasure',
    'double',
    'double_win',
    'treasure_unlock',
    'double_end_with_treasure',
    'obtain_item',
    'play_again',
    'won_hand',
    'tie',
    'win'
]

transitions = {}
_state = None
_expected_next_state = None

state_images = {}
for state in states:
    state_images[state] = cv2.imread('states/{}.png'.format(state))

def get(img):
    diffs = []
    for state in states:
        roi = pos.get(img, 'states', state)
        diffs.append([cv2.absdiff(state_images[state], roi).mean(), state])

    diffs.sort(key=lambda x: x[0])

    if diffs[0][0] < 20:
        return diffs[0][1]


    return None


def enter(new_state, frame):
    global _last_state, _state

    print 'CHANGESTATE,{},{}'.format(new_state, _state)
    if _state != new_state:
        logging.info('enter state: ' + new_state)

        if new_state in transitions:
            transitions[new_state](frame, _state)

        _state = new_state





