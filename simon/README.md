# Yet Another Simon Clone

An implementation of the Simon game, because everybody does it sooner or later!

- 4 Skill Levels
    - Level 1 : 8 lights
    - Level 2 : 14 lights
    - Level 3 : 20 lights
    - Level 4 : 31 lights
- Flashing speeds up at 5, 9, and 13 lights

For a demo, you can [play with a virtual version on Wokwi](https://wokwi.com/projects/390970795638773761) -- in the circuit area, press the green triangle button to start the program running and the grey square to stop it again. You can use keyboard input for "pressing the buttons": `1 = Red, 2 = Green, 3 = Blue, 4 = Yellow`.

## @Todo

- Save high score

## Requirements

The following is a required module for a 128x64 monochrome I2C OLED display:

- SSD1306 Driver [MicroPython repo](https://github.com/micropython/micropython-lib/)
    - [`ssd1306.py`](https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/display/ssd1306/ssd1306.py)
