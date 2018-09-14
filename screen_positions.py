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
    ]
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
