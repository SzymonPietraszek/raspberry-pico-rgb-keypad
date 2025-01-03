import time
import picokeypad
import random


keypad = picokeypad.PicoKeypad()
keypad.set_brightness(0.1)

NUM_PADS = keypad.get_num_pads()


def level_color(key: int):
    return (0x10 * key, 0xf0 - 0x10 * key, 0x00)


def get_buttons(button_states: int) -> list[int]:
    button = 0
    buttons = []
    while button_states > 0:
        if button_states & 1 > 0:
            buttons.append(button)
        button += 1
        button_states >>= 1
    return buttons


for key in range(0, NUM_PADS):
    keypad.illuminate(key, *level_color(key))
keypad.update()

time.sleep(1)

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

    last_button_states = 0
    while True:
        button_states = keypad.get_button_states()
        if last_button_states != button_states:  # buttons has changed
            last_button_states = button_states
            if button_states > 0:
                buttons = get_buttons(button_states)
                if len(buttons) == 1:
                    level = buttons[0]
                    break
        time.sleep(0.1)

    for i in range(0, NUM_PADS):  
        keypad.illuminate(i, *level_color(level))
    keypad.update()

    time.sleep(1)

    for i in range(0, NUM_PADS):
        keypad.illuminate(i, 0, 0, 0)
    keypad.update()
    keys = set(range(0, NUM_PADS))

    i = 0
    while len(keys) > 0:
        button_states = keypad.get_button_states()

        for button in get_buttons(button_states):
            keypad.illuminate(button, 0, 0, 0)
            keys.add(button)

        if i % (16 - level) == 0:
            key = random.choice(list(keys))
            keys.remove(key)
            keypad.illuminate(key, *level_color(level))

        keypad.update()
        time.sleep(0.1)
        i += 1

    for key in [0, 3, 5, 6, 9, 10, 12, 15]:  # red X sign
        keypad.illuminate(key, 0xff, 0, 0)
    for key in [1, 2, 4, 7, 8, 11, 13, 14]:
        keypad.illuminate(key, 0, 0, 0)
    keypad.update()
    time.sleep(2)

    while True:
        if keypad.get_button_states() != 0:
            break
        time.sleep(0.1)
