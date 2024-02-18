# Binary Clock

A simple binary clock using LEDs and a Raspberry Pi Pico W.

For a quick demo, you can [play with a virtual version on Wokwi](https://wokwi.com/projects/389796647886494721) -- in the circuit area, press the green triangle button to start the program running and the grey square to stop it again.

> **Note**: In the above Wokwi demo, the WiFi access simulation for the Pico W does not currently function. Parts of the code relating to this are commented out and labelled. It does mean you will have to manually update the RTC in the code to reflect your local time.

There is also a [demo with 'NeoPixels'](https://wokwi.com/projects/389995570833197057) (a brand of individually-addressable RGB LEDs) which uses considerably fewer GPIO pins (x3 instead of x17, not including power and ground pins).  **Note** if building this yourself, you'll need a capacitor (approx 1000µF) between the power supply and NeoPixels, especially if using a higher-powered power source than the 5V provided by VBUS pin of the Pico board alone.

## @Todo

### More intelligent synchronisation routine

If we only sync at fixed periods from the moment the clock is booted (switched on) then we may miss when the clocks go forward/back for BST/GMT switch by several hours -- not helpful!

- Sync on boot-up and after that:
    - Sync at 01:00:01 from Jan-Jun (to correct for change to BST in March)
    - Sync at 02:00:01 from Jul-Dec (to correct for change to GMT in October)
