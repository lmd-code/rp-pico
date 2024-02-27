# Quiz Buzzer

Simple implementation of a four button "fastest person first" system.

Button press:

- Disables other buzzers
- Turns on matching colour LED
- Plays buzzer tune (different tune for each button)
- Shows the button being pressed (colour label) on the OLED display

For a quick demo, you can [play with a virtual version on Wokwi](https://wokwi.com/projects/389155923011352577) -- in the circuit area, press the green triangle button to start the program running and the grey square to stop it again. When started, press the buttons on the breadboard to see what happens. Click on the "Docs" link for more help using the Wokwi app.

## Requirements

The following are required modules for a 128x64 monochrome I2C OLED display:

- SSD1306 Driver [MicroPython repo](https://github.com/micropython/micropython-lib/)
    - [`ssd1306.py`](https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/display/ssd1306/ssd1306.py)
- The following files from the [Micropython Font-to-Py repo](https://github.com/peterhinch/micropython-font-to-py)
    - [`courier20.py`](https://github.com/peterhinch/micropython-font-to-py/blob/master/writer/courier20.py) (larger font than the ssd1306 default)
    - [`writer_minimal.py`](https://github.com/peterhinch/micropython-font-to-py/blob/master/writer/old_versions/writer_minimal.py) (enables use of larger font)
