# Binary Clock

A simple binary clock using LEDs and a Raspberry Pi Pico W.

For a quick demo, you can [play with a virtual version on Wokwi](https://wokwi.com/projects/389796647886494721) -- in the circuit area, press the green triangle button to start the program running and the grey square to stop it again.

> **Note**: In the above Wokwi demo, the WiFi access simulation for the Pico W does not currently function. Parts of the code relating to this are commented out and labelled. It does mean you will have to manually update the RTC in the code to reflect your local time.

There is also a [demo with 'NeoPixels'](https://wokwi.com/projects/389995570833197057) (a brand of individually-addressable RGB LEDs) which uses considerably fewer GPIO pins (x3 instead of x17, not including power and ground pins).  **Note** if building this yourself, you'll need a capacitor (approx 1000µF) between the power supply and NeoPixels, especially if using a higher-powered power source than the 5V provided by VBUS pin of the Pico board alone.

## A note on synchronisation routine

To account for when the clocks change (for daylight savings and back), synchronisation occurs at different times depending on the month:

- Sync on boot-up and after that:
    - Sync at `01:00:01` all months except October (clocks go forward 1 hr to BST last Sunday in March)
    - Sync at `02:00:01` in October only (clocks go back 1 hr to GMT last Sunday in October)

The reason for not just synching at `02:00` for all months is because that one hour discrepency when the clock goes forward at `01:00` in March might be important for somebody!

Actual dates and times, or even if clocks change at all, will vary depending on where you live in the world.

## @Todo

### [ ] Multithreading

Run the sync route in a separate thread so that waiting for WLAN connection doesn't block clock action.
