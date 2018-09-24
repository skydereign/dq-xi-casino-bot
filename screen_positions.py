positions = {
    "cards": [
        [94,  237, 28, 28],
        [271, 237, 28, 28],
        [447, 237, 28, 28],
        [624, 237, 28, 28],
        [800, 237, 28, 28]
    ],

    "keep_icons": [
        [110, 415, 66, 14],
        [286, 415, 66, 14],
        [463, 415, 66, 14],
        [639, 415, 66, 14],
        [815, 415, 66, 14]
    ],

    "focused": [
        [92,  420, 11, 2],
        [268, 420, 11, 2],
        [445, 420, 11, 2],
        [621, 420, 11, 2],
        [797, 420, 11, 2]
    ],

    "deal_focused": [452, 458, 11, 3],

    "tokens":[339, 527, 120, 20],
    "stake":[535, 528, 120, 20],

    "got_hands": [
        [397,  99, 30, 14], # Royal Jelly Flush  50000
        [397, 120, 30, 14], # Royal Flush        10000 
        [397, 141, 30, 14], # Five of a Kind      5000
        [397, 162, 30, 14], # Straight Flush      2000
        [397, 183, 30, 14], # Four of a Kind      1000
    
        [670,  99, 30, 14], # Full House           500
        [670, 120, 30, 14], # Flush                400
        [670, 141, 30, 14], # Straight             300
        [670, 162, 30, 14], # Three of a Kind      100
        [670, 183, 30, 14]  # Two Pair             100
    ],

    "dialog_box": [197, 469, 603, 102],

    "states":{
        'start_red':[410, 385, 180, 90], # "Change Stake"
        'start_blue':[410, 385, 180, 90], # "Change Stake"
        'hand_dealt':[461, 447, 71, 29], # "Deal"

        'loss':[212, 488, 144, 12], # "What a shame! Do you want to play again?"
        'double_prompt':[212, 488, 144, 12], # "You can play Double or Nothing"
    
        'treasure':[212, 488, 144, 12], # "You've found a treasure"
        'double':[212, 488, 144, 12], # "Try to pick a higher card"
        'double_win':[212, 488, 144, 12], # "Nicely played! You win"
        'treasure_unlock':[212, 488, 144, 12], # "Well done! You've removed all the locks!"
        'double_end_with_treasure':[212, 488, 144, 12], # "It's the moment you've been waiting for",
        'obtain_item':[212, 488, 144, 12], # "You obtain a piece of"
        'play_again':[212, 488, 144, 12], # "Do you want to play poker again?"
        'won_hand':[212, 488, 144, 12], # "Congratulations! You got"
        'tie':[212, 488, 144, 12], # "It's the same value as the last card!"
        'treasure_trove':[212, 488, 144, 12], # "You receive"
    
        'win':[212, 488, 69, 12] # "You win"
    }
}


def get_num(name):
    if type(positions[name]) == list:
        return len(positions[name])

    return 0


def get(img, name, index=None):
    position = positions[name] if index is None else positions[name][index]
    right = position[0] + position[2]
    bottom = position[1] + position[3]

    return img[position[1]:bottom, position[0]:right]


if __name__ == '__main__':
    import cv2
    
    img = cv2.imread('state_base/congrats_two_pair.png')
    cv2.imshow('frame', get(img, 'cards', ''))
    cv2.waitKey()
