"""
A game  of Simon

- 4 Buttons (R, G, B, Y)
- 4 LEDs (R, G, B, Y)
- 1 Buzzer
- 1 OLED Display
"""

from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C
import random, time, sys

BTNLED_GPIO = [
    # Red / A3
    {'btn_pin': 6, 'led_pin': 7, 'btn': None, 'led': None, 'tone': 220.00, 'btn_on': False},

    # Green / E3
    {'btn_pin': 8, 'led_pin': 9, 'btn': None, 'led': None, 'tone': 164.81, 'btn_on': False},

    # Blue / E4
    {'btn_pin': 10, 'led_pin': 11, 'btn': None, 'led': None, 'tone': 329.63, 'btn_on': False},

    # Yellow / C#4
    {'btn_pin': 12, 'led_pin': 13, 'btn': None, 'led': None, 'tone': 277.18, 'btn_on': False},
]

# Dictionary of button pins and their index
BTN_PINS = {}
for i, p in enumerate(BTNLED_GPIO):
    _btn_pin = p['btn_pin']
    BTN_PINS[_btn_pin] = i


BUZZER_PIN = 22
BUZZER_DUTY = 3000 # PWM duty cycle - higher number = louder (max 65535)
BUZZER_TUNES = {
    'correct': ([1047, 100], [1319, 100], [1568, 100], [2093, 100]), # frequency (hz), duration (ms)
    'loser': ([73, 250], [0, 100], [55, 650]), # 0 hz = a rest (0 volume)
    'winner': ([783, 200], [0, 50], [783, 150], [0, 50], [1046, 550])
}

OLED_PINS = {'SDA': 16, 'SCL': 17} # I2C Pins
SCREEN = {'width': 128, 'height': 64, 'v_padding': 2, 'working_h': 0} # Screen width and height (px)
SCREEN['working_h'] = SCREEN['height'] - (SCREEN['v_padding'] * 2) # working screen height 

FONT = {'width': 8, 'height': 8, 'padding': 1, 'line_height': 0} # Font width and height (px)
FONT['line_height'] = FONT['height'] + (FONT['padding'] * 2) # line height

SCRN_COLS = int(SCREEN['width'] / FONT['width'])
SCRN_ROWS = int(SCREEN['working_h'] / FONT['line_height'])

# Functions

def led_on(pressed: int = -1):
    """ Turn on LED for specified button index, or turn on all LEDs """
    if (pressed > -1):
        BTNLED_GPIO[pressed]['led'].value(1)
    else:
        for led in range(len(BTNLED_GPIO)):
            BTNLED_GPIO[led]['led'].value(1)   


def led_off(pressed: int = -1):
    """ Turn off LED for specified button index, or turn off all LEDs """
    if (pressed > -1):
        BTNLED_GPIO[pressed]['led'].value(0)
    else:
        for led in range(len(BTNLED_GPIO)):
            BTNLED_GPIO[led]['led'].value(0)


def buzzer_on(hz: int):
    """ Turn on buzzer at specified frequency (Hz) """
    buzzer.freq(hz)
    buzzer.duty_u16(BUZZER_DUTY)


def buzzer_off():
    """ Turn off buzzer """
    buzzer.duty_u16(0)


def play_buzzer_tune(tune: str):
    """ Play a tune for certain game events """
    for hz, duration in BUZZER_TUNES[tune]:
        if (hz > 0):
            buzzer.freq(hz)
            buzzer.duty_u16(BUZZER_DUTY)
        else:
            buzzer_off()
        time.sleep_ms(duration)
    buzzer_off()


def display_text(msg: str):
    """ Display specified text centred on screen horizontally and vertically """
    if '\n' in msg:
        words = msg.split('\n')
    else:
        words = msg.split()

    lines = ['']
    row = 0

    for word in words:
        row_len = len(lines[row])
        word_len = len(word)

        if (row_len > 0): word_len += 1 # +1 for space

        if row_len + word_len <= SCRN_COLS:
            if (row_len > 0): lines[row] += ' ' # add space
            lines[row] += word
        else:
            row += 1
            if (row < SCRN_ROWS):
                lines.append(word)
        if row == SCRN_ROWS:
            break

    display.fill(0)
    num_lines = len(lines)

    y = int((SCREEN['working_h'] - (num_lines * FONT['line_height'])) / 2) + SCREEN['v_padding']

    for line in range(num_lines):
        x = int((SCREEN['width'] - (FONT['width'] * len(lines[line]))) / 2)
        display.text(lines[line].upper(), x, y + 1)
        y = y + FONT['line_height']
    display.show()


def display_clear():
    """ Clear display """
    display.fill(0)
    display.show()


def poll_btns():
    """ Poll button inputs to see if and which one was pressed """
    global BTNLED_GPIO
    btn_pressed = -1 # no button pressed
    for btn in range(len(BTNLED_GPIO)):
        if BTNLED_GPIO[btn]['btn'].value() == 1 and not BTNLED_GPIO[btn]['btn_on']:
            BTNLED_GPIO[btn]['btn_on'] = True
            return btn

    return btn_pressed


def btn_handler(pin):
    """ Interrupt handler to remove 'btn_on' bool condition from button on release """
    global BTNLED_GPIO
    btn_pin = int(str(pin)[8:10].replace(',', '')) # get pressed button pin number
    btn_pressed = BTN_PINS[btn_pin] # Index of pin
    BTNLED_GPIO[btn_pressed]['btn_on'] = False


def sequence_action(idx: int, speed: int):
    """ Run LED/Buzzer sequence """
    led_on(idx)
    buzzer_on(int(BTNLED_GPIO[idx]['tone']))
    time.sleep_ms(speed)
    buzzer_off()
    led_off(idx)
    time.sleep_ms(speed)


def get_random_sequence(seq_len: int) -> list:
    """
    Generate a random sequence of colours by index

    Parameters:
    -----------

    seq_len: int
        Length of sequence to generate
    """

    rpts = {} # track repeats
    last_item = -1 # track last selected item
    sq = [] # selected sequence

    for _ in range(seq_len):
        # If item has been selected 2x in a row, loop until new item is selected
        while True:
            item = random.randrange(0, num_colours) # 0 - 3 inclusive

            if item == last_item:
                if (rpts[item] < 2):
                    rpts[item] += 1 # increment repeat counter
                    break # break loop
            else:
                rpts[item] = 1 # set/reset repeat counter
                break # break loop

        last_item = item
        sq.append(item)

    return sq


# Setup Pin objects
for btnled in BTNLED_GPIO:
    btnled['btn'] = Pin(btnled['btn_pin'], Pin.IN, Pin.PULL_DOWN)
    btnled['btn'].irq(trigger = Pin.IRQ_FALLING, handler = btn_handler) # on button press 1 -> 0
    btnled['led'] = Pin(btnled['led_pin'], Pin.OUT)

buzzer = PWM(Pin(BUZZER_PIN))

i2c = I2C(0, sda = Pin(OLED_PINS['SDA']), scl = Pin(OLED_PINS['SCL']), freq = 400000)
time.sleep(1) # Allow I2C to kick in
display = SSD1306_I2C(SCREEN['width'], SCREEN['height'], i2c)

##### Start game interface

try:
    while True:
        ##### Setup game vars

        play_game = False # flag game start
        pressed = -1 # index of pressed button
        num_colours = len(BTNLED_GPIO) # number of colours (leds/buttons)
        levels = [8, 14, 20, 31] # difficulty levels = length of sequence
        current_level = 0 # current player level (zero-indexed!)
        current_round = 0 # Current round in level
        speed_increases = [5, 9, 13] # item in sequence at which speed increases
        speed_decrement = 100 # milliseconds deducted at speed increase
        speed_start = 500 # start at 500 milliseconds between items
        speed_current = speed_start
        sequence = [] # store randomly selected sequence

        # Prep game hardware
        buzzer_off()
        led_off()
        display_clear()

        ##### Wait for player input
        display_text('Press any button to play the game')
        while play_game == False:
            if poll_btns() > -1:
                play_game = True

        ##### Game play

        sequence_len = levels[current_level]

        display_text("LEVEL " + str(current_level + 1) + "\n(" + str(sequence_len) + " ROUNDS)")
        time.sleep(1)
        for _ in reversed(range(5)):
            display_text('... ' + str(_ + 1) + ' ...')
            time.sleep(1)


        # Select full random sequence
        sequence = get_random_sequence(sequence_len)

        score = 0 # keep score

        # Loop each level
        for game_round in range(sequence_len):
            current_round = game_round + 1 # account for zero indexing

            if (current_round in speed_increases):
                speed_current -= speed_decrement # increase speed (decrease sleep delay)

            display_text('Round ' + str(current_round))

            time.sleep(1)

            # Play current sequence
            for s in range(current_round):
                sequence_action(sequence[s], speed_current) # flash led and player buzzer tone

            # Player input
            req_btn_presses = current_round # required no. button presses (= current round)
            btn_presses = 0 # current count of button presses
            player_err = False # flag when player makes an error

            display_text('Your turn')

            # Loop until reaching required button presses or player makes an error
            while (btn_presses < req_btn_presses):
                pressed = poll_btns() # Get index of the pressed button
                if pressed > -1:
                    sequence_action(pressed, speed_current) # flash/buzz!
                    if (pressed != sequence[btn_presses]):
                        player_err = True # incorrect button pressed
                        break # break out of button press loop
                    btn_presses += 1 # increment button press counter
                    pressed = -1 # reset pressed button

            # Player input over, if there was an error, immediately end the current game
            if player_err:
                display_text('Incorrect!')
                break # stop looping rounds and go to game over

            # No errors, then go to next round (if there is one)
            score += 1 # increment score
            display_text('Correct!')
            play_buzzer_tune('correct')
            time.sleep(1)

        ##### GAME OVER

        score_txt = str(score) + "/" + str(sequence_len)

        # Play/show either loser/winner tune/text
        if player_err:
            display_text("You got " + score_txt + "\nBetter luck\nnext time!?")
            play_buzzer_tune('loser')
        else:
            display_text("You got " + score_txt + "\nWell done!")
            play_buzzer_tune('winner')
        
        time.sleep(2) # pause two secs, then loop back to start

except KeyboardInterrupt:
    buzzer_off()
    led_off()
    display_clear()
    sys.exit(0)