from machine import Pin, RTC
from neopixel import NeoPixel
from localconfig import WIFI_SSID, WIFI_PW
import time, sys, network, urequests

# World Time Clock API to synchronise Pico's RTC
TIME_API_URI = "http://worldtimeapi.org/api/ip"
SYNC_PERIOD = 60*60*24 # sync once a day

# Set each NeoPixel strip ('npx') and associate an RGB colour
STRIP_H = {'npx': NeoPixel(Pin(27), 5), 'rgb': (255,0,0)} # Hours (24-hr format) / Red
STRIP_M = {'npx': NeoPixel(Pin(21), 6), 'rgb': (0,255,0)} # Minutes / Green
STRIP_S = {'npx': NeoPixel(Pin(17), 6), 'rgb': (0,0,255)} # Seconds / Blue

LED_OFF = (0,0,0) # Black = off/unlit


def connect_wifi():
    """
    Connect to WiFi network
    """

    print("Connecting to WiFi", end="")
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PW) # SSD/PW from file not committed to Git repo
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Connected!")


def sync_rtc(rtc, blocking = True):
    """
    Use WiFi to synchronise Pico RTC with World Time Clock

    Parameters
    ----------
    rtc : RTC
        Real Time Clock object
    blocking : bool
        When true (default), wait for a response (used on first connection), when false, close connection until next sync cycle
    """

    # Make WiFi connection
    connect_wifi()

    response = None
    while True:
        try:
            response = urequests.get(TIME_API_URI)
            break
        except:
            if blocking:
                response.close()
                continue
            else:
                response.close()
                return

    json = response.json()
    current_time = json["datetime"]
    the_date, the_time = current_time.split("T")
    year, month, mday = [int(x) for x in the_date.split("-")]
    the_time = the_time.split(".")[0]
    hours, minutes, seconds = [int(x) for x in the_time.split(":")]
    week_day = json["day_of_week"]

    response.close()
    wlan.disconnect()
    rtc.datetime((year, month, mday, week_day, hours, minutes, seconds, 0))


def toggle_leds(hrs: int, mins: int, secs: int):
    """
    Toggle LEDs on/off according to current time

    Parameters
    ----------
    hrs : int
        Hours in 24-hour format (0 - 23)
    mins : int
        Minutes
    secs : int
        Seconds
    """

    bin_hrs = "{0:0{len}b}".format(hrs, len=STRIP_H['npx'].n) # hours in binary
    bin_mins = "{0:0{len}b}".format(mins, len=STRIP_M['npx'].n) # minutes in binary
    bin_secs = "{0:0{len}b}".format(secs, len=STRIP_S['npx'].n) # seconds in binary

    print(f"{hrs:0>2}:{mins:0>2}:{secs:0>2} - {bin_hrs} : {bin_mins} : {bin_secs}")

    # Set hours
    for led in range(STRIP_H['npx'].n):
        if (int(bin_hrs[led]) == 1):
            STRIP_H['npx'][led] = STRIP_H['rgb']
        else:
            STRIP_H['npx'][led] = LED_OFF
    STRIP_H['npx'].write()

    # Set minutes
    for led in range(STRIP_M['npx'].n):
        if (int(bin_mins[led]) == 1):
            STRIP_M['npx'][led] = STRIP_M['rgb']
        else:
            STRIP_M['npx'][led] = LED_OFF
    STRIP_M['npx'].write()

    # Set seconds
    for led in range(STRIP_S['npx'].n):
        if (int(bin_secs[led]) == 1):
            STRIP_S['npx'][led] = STRIP_S['rgb']
        else:
            STRIP_S['npx'][led] = LED_OFF
    STRIP_S['npx'].write()

def clear_leds():
    """
    Turn all the LEDs off
    """
    for led in range(STRIP_H['npx'].n):
        STRIP_H['npx'][led] = LED_OFF
    STRIP_H['npx'].write()

    for led in range(STRIP_M['npx'].n):
        STRIP_M['npx'][led] = LED_OFF
    STRIP_M['npx'].write()

    for led in range(STRIP_S['npx'].n):
        STRIP_S['npx'][led] = LED_OFF
    STRIP_S['npx'].write()


################################################################################
# Run Program

try:
    # Init WLAN
    wlan = network.WLAN(network.STA_IF)

    # Init the Real Time Clock
    rtc = RTC()

    # Synchronise the RTC with the World Clock
    sync_rtc(rtc)

    # Init the sync countdown timer
    sync_countdown = SYNC_PERIOD

    # Make sure all LEDS are off
    clear_leds()
    
    while True:
        Y, M, D, W, HH, MM, SS, MS = rtc.datetime() # Get current timestamp
        toggle_leds(HH, MM, SS) # Toggle LEDs on/off according to time

        # Synchronise the RTC if countdown has elapsed
        if sync_countdown == 0:
            sync_countdown = SYNC_PERIOD # Reset timer
            sync_rtc(rtc, blocking=False) # Don't block this time

        sync_countdown -= 1 # Decrement timer

        time.sleep(1) # Wait 1 second
    
except KeyboardInterrupt:
    clear_leds()
    sys.exit(0)