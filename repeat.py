import time
import picokeypad
import random


keypad = picokeypad.PicoKeypad()
keypad.set_brightness(0.1)

NUM_PADS = keypad.get_num_pads()


def level_color(key: int):
    return (0x10 * key, 0xf0 - 0x10 * key, 0x00)


def get_keys(button_states: int) -> list[int]:
    button = 0
    keys = []
    while button_states > 0:
        if button_states & 1 > 0:
            keys.append(button)
        button += 1
        button_states >>= 1
    return keys


def wait_for_one_key() -> int:
    while True:
        button_states = keypad.get_button_states()
        keys = get_keys(button_states)
        if len(keys) == 1:
            return keys[0]
        time.sleep(0.1)


def turn_off_all_keys():
    for i in range(0, NUM_PADS):
        keypad.illuminate(i, 0, 0, 0)
    keypad.update()


def ok_sign():
    for key in [3, 6, 8, 10, 13]:
        keypad.illuminate(key, 0, 0xff, 0)
    for key in [0, 1, 2, 4, 5, 7, 9, 11, 12, 14, 15]:
        keypad.illuminate(key, 0, 0, 0)
    keypad.update()


def x_sign():
    for key in [0, 3, 5, 6, 9, 10, 12, 15]:
        keypad.illuminate(key, 0xff, 0, 0)
    for key in [1, 2, 4, 7, 8, 11, 13, 14]:
        keypad.illuminate(key, 0, 0, 0)
    keypad.update()


while True:
    for key in range(0, NUM_PADS):
        for i in range(0, NUM_PADS):
            keypad.illuminate(i, 0x00, 0x00, 0x00)
        keypad.illuminate(key, *level_color(key))
        keypad.update()
        time.sleep(0.1)

    for key in range(0, NUM_PADS):  # lit all keys to theirs level/color
        keypad.illuminate(key, *level_color(key))
    keypad.update()

    level = wait_for_one_key()

    for i in range(0, NUM_PADS):
        keypad.illuminate(i, *level_color(level))
    keypad.update()
    time.sleep(1)
    turn_off_all_keys()

    for num_of_keys_to_lit in range(1, NUM_PADS + 1):
        keys = set(range(0, NUM_PADS))
        lit_keys = []
        for i in range(num_of_keys_to_lit):
            key = random.choice(list(keys))
            keys.remove(key)
            lit_keys.append(key)
            keypad.illuminate(key, *level_color(level))
            keypad.update()
            time.sleep(0.1 * (16 - level))

            keypad.illuminate(key, 0, 0, 0)
            keypad.update()
            time.sleep(0.1 * (16 - level))

        clicked_keys = []
        while True:
            key = wait_for_one_key()
            if key in clicked_keys:
                continue

            keypad.illuminate(key, *level_color(level))
            keypad.update()
            clicked_keys.append(key)

            time.sleep(0.1)

            if len(clicked_keys) == len(lit_keys):
                break

        if clicked_keys == lit_keys:
            ok_sign()
            time.sleep(2)
            turn_off_all_keys()
        else:
            x_sign()
            time.sleep(2)
            turn_off_all_keys()
            break

    while True:
        if keypad.get_button_states() != 0:
            break
        time.sleep(0.1)
