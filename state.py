import screen_positions as pos
import logging
import time
import cv2

states = [
    'start_red',
    'start_blue',
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
    'treasure_trove',
    'win'
]

transitions = {}
_state = None
_expected_next_states = []

state_images = {}
for state in states:
    state_images[state] = cv2.imread('states/{}.png'.format(state), cv2.IMREAD_UNCHANGED)

def get(img):
    print('state.get')
    diffs = []

    for state in states:
        roi = pos.get(img, 'states', state)
        
        mean = cv2.absdiff(state_images[state], roi).mean()
        diff = [mean, state]
        diffs.append(diff)
        
    diffs.sort(key=lambda x: x[0])

    if diffs[0][0] < 30:
        return diffs[0][1]


    return None


def enter(new_state, frame, initial=False):
    global _last_state, _state, _expected_next_states

    if new_state:
        logging.info('change state,{},{}'.format(new_state, _state))
        if _state != new_state:
            if not initial and new_state not in _expected_next_states:
                logging.info('error,entered unexpected state')
            
            if new_state in transitions:
                _expected_next_states = transitions[new_state](frame, _state)
        
            _state = new_state
        else:
            time.sleep(0.5)
            _expected_next_states = transitions[new_state](frame, _state)






