positions = {
    "cards": [
        [94,  237, 28, 28],
        [271, 237, 28, 28],
        [447, 237, 28, 28],
        [624, 237, 28, 28],
        [800, 237, 28, 28]
    ],
    
    "states":{
        'start':[410, 385, 180, 90], # "Change Stake"
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
