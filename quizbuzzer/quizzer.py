from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C
import courier20 # custom font
from writer_minimal import Writer # custom font display
import time, sys

BTNLED_GPIO = [
    {'btn_pin': 18, 'led_pin': 10, 'btn': None, 'led': None, 'buzzer': 'r', 'label': 'RED',},
    {'btn_pin': 19, 'led_pin': 11, 'btn': None, 'led': None, 'buzzer': 'g', 'label': 'GREEN',},
    {'btn_pin': 20, 'led_pin': 12, 'btn': None, 'led': None, 'buzzer': 'b', 'label': 'BLUE',},
    {'btn_pin': 21, 'led_pin': 13, 'btn': None, 'led': None, 'buzzer': 'y', 'label': 'YELLOW',},
]

BUZZER_PIN = 15
BUZZER_DUTY = 3000 # PWM duty cycle - higher number = louder (max 65535)

# Buzzer "tunes" (simple arpeggios) - each integer is a frequency (Hz) corresponding to a musical note pitch
BUZZER_FREQ = {
    'r': (131, 165, 196, 262),
    'g': (262, 196, 165, 131),
    'b': (1047, 1319, 1568, 2093),
    'y': (2093, 1568, 1319, 1047),
}

OLED_PINS = {'SDA': 0, 'SCL': 1} # I2C Pins
SCREEN = {'width': 128, 'height': 64} # Screen width and height (px)
FONT = {'width': 14, 'height': 20} # Font width and height (px)

# Index of pressed button corresponds to index of matching LED and buzzer tune
pressed = 0

# Setup Pin objects

for btnled in BTNLED_GPIO:
    btnled['btn'] = Pin(btnled['btn_pin'], Pin.IN, Pin.PULL_DOWN)
    btnled['led'] = Pin(btnled['led_pin'], Pin.OUT)

buzzer = PWM(Pin(BUZZER_PIN))

i2c = I2C(0, sda = Pin(OLED_PINS['SDA']), scl = Pin(OLED_PINS['SCL']), freq = 400000)
time.sleep(1) # Allow I2C to kick in
display = SSD1306_I2C(SCREEN['width'], SCREEN['height'], i2c)
font_writer = Writer(display, courier20, False)

# Functions

def poll_btns():
    """
    Poll each button to see if it was pressed as soon as the first button press is detected
    store it's index and return True, otherwise return False until next scan
    """
    global pressed
    for btn in range(len(BTNLED_GPIO)):
        if (BTNLED_GPIO[btn]['btn'].value() == 1):
            pressed = btn # Update index of pressed button
            return True # A button is pressed, return immediately
    return False # No button pressed

def buzzer_on(pressed: int):
    """Play the buzzer tune for specified button index"""
    buzzer_id = BTNLED_GPIO[pressed]['buzzer']
    for hz in BUZZER_FREQ[buzzer_id]:
        buzzer.freq(hz)
        buzzer.duty_u16(BUZZER_DUTY)
        time.sleep_ms(100)

def buzzer_off():
    buzzer.duty_u16(0)

def led_on(pressed: int = -1):
    """Turn on LED for specified button index, or turn on all LEDs"""
    if (pressed > -1):
        BTNLED_GPIO[pressed]['led'].value(1)
    else:
        for led in range(len(BTNLED_GPIO)):
            BTNLED_GPIO[led]['led'].value(1)        

def led_off(pressed: int = -1):
    """Turn off LED for specified button index, or turn off all LEDs"""
    if (pressed > -1):
        BTNLED_GPIO[pressed]['led'].value(0)
    else:
        for led in range(len(BTNLED_GPIO)):
            BTNLED_GPIO[led]['led'].value(0)

def display_text(pressed: int):
    """Display label for specified button index"""
    txt = BTNLED_GPIO[pressed]['label']
    x = int((SCREEN['width'] - (FONT['width'] * len(txt))) / 2)
    y = int((SCREEN['height'] - FONT['height']) / 2)
    display.fill(0)
    font_writer.set_textpos(x, y)
    font_writer.printstring(txt)
    display.show()

def display_clear():
    """Clear display"""
    display.fill(0)
    display.show()

# Run program
try:
    while True:
        if (poll_btns()):
            led_on(pressed)
            display_text(pressed)
            buzzer_on(pressed)
        else:
            buzzer_off()
            display_clear()
            led_off()

        time.sleep_ms(100)
except KeyboardInterrupt:
    buzzer_off()
    display_clear()
    led_off()
    sys.exit(0)