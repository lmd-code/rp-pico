# Yet Another Simon Clone

An implementation of the Simon game, because everybody does it sooner or later!

- 4 Skill Levels
    - L1 : 8 lights
    - L2 : 14 lights
    - L3 : 20 lights
    - L4 : 31 lights
- Flashing speeds up after 5, 9, and 13 lights

**Currently only level 1 is playable.**

## @Todo

- Add level selector
- Save high score

## Requirements

The following is a required module for a 128x64 monochrome I2C OLED display:

- SSD1306 Driver [MicroPython repo](https://github.com/micropython/micropython-lib/)
    - [`ssd1306.py`](https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/display/ssd1306/ssd1306.py)
