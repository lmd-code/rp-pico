from machine import Pin, RTC
from libs.localconfig import WIFI_SSID, WIFI_PW
import time, sys, network, urequests

# World Time Clock API to synchronise Pico's RTC - set this to your own timezone
TIME_API_URI = "http://worldtimeapi.org/api/timezone/Europe/London"
# Alternatively use IP address if it is the same as your timezone
#TIME_API_URI = "http://worldtimeapi.org/api/ip"

# Synchronisation time checks (applies to UK timezone, where we have summer daylight savings)
SYNC_TIMES = {
    'default': '01:00:01', # Most of the year (clocks go forward to BST at 01:00 last Sun in Mar)
    'october': '02:00:01', # October only (clocks go back to GMT at 02:00 last Sun in Oct)
}

# Hour LED pins
GPIO_LED_H = [
    {'pin': 18, 'led': None},
    {'pin': 19, 'led': None},
    {'pin': 20, 'led': None},
    {'pin': 21, 'led': None},
    {'pin': 22, 'led': None},
]

# Minute LED pins
GPIO_LED_M = [
    {'pin': 13, 'led': None},
    {'pin': 12, 'led': None},
    {'pin': 11, 'led': None},
    {'pin': 10, 'led': None},
    {'pin': 9, 'led': None},
    {'pin': 8, 'led': None},
]

# Second LED pins
GPIO_LED_S = [
    {'pin': 7, 'led': None},
    {'pin': 6, 'led': None},
    {'pin': 5, 'led': None},
    {'pin': 4, 'led': None},
    {'pin': 3, 'led': None},
    {'pin': 2, 'led': None},
]

# Number of hour, min, sec LEDs - each LED represents one binary bit
NUM_LEDS_H = len(GPIO_LED_H)
NUM_LEDS_M = len(GPIO_LED_M)
NUM_LEDS_S = len(GPIO_LED_S)


def connect_wifi():
    """
    Connect to WiFi network
    """

    print("Connecting to WiFi", end="")
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PW) # SSID/PW from file not committed to Git repo
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

    bin_hrs = "{0:0{len}b}".format(hrs, len=NUM_LEDS_H) # hours in binary
    bin_mins = "{0:0{len}b}".format(mins, len=NUM_LEDS_M) # minutes in binary
    bin_secs = "{0:0{len}b}".format(secs, len=NUM_LEDS_S) # seconds in binary

    print(f"{hrs:0>2}:{mins:0>2}:{secs:0>2} - {bin_hrs} : {bin_mins} : {bin_secs}")

    # Set hours
    for led in range(NUM_LEDS_H):
        GPIO_LED_H[led]['led'].value(int(bin_hrs[led]))

    # Set minutes
    for led in range(NUM_LEDS_M):
        GPIO_LED_M[led]['led'].value(int(bin_mins[led]))

    # Set Seconds
    for led in range(NUM_LEDS_S):
        GPIO_LED_S[led]['led'].value(int(bin_secs[led]))


def clear_leds():
    """
    Turn all the LEDs off
    """
    for led in range(NUM_LEDS_H):
        GPIO_LED_H[led]['led'].value(0)
    for led in range(NUM_LEDS_M):
        GPIO_LED_M[led]['led'].value(0)
    for led in range(NUM_LEDS_S):
        GPIO_LED_S[led]['led'].value(0)


################################################################################
# Run Program

try:
    # Make LED pin connections
    for i in range(NUM_LEDS_H):
        GPIO_LED_H[i]['led'] = Pin(GPIO_LED_H[i]['pin'], Pin.OUT)

    for i in range(NUM_LEDS_M):
        GPIO_LED_M[i]['led'] = Pin(GPIO_LED_M[i]['pin'], Pin.OUT)

    for i in range(NUM_LEDS_S):
        GPIO_LED_S[i]['led'] = Pin(GPIO_LED_S[i]['pin'], Pin.OUT)

    # Init WLAN
    wlan = network.WLAN(network.STA_IF)

    # Init the Real Time Clock
    rtc = RTC()

    # Synchronise the RTC with the World Clock
    sync_rtc(rtc)

    # Make sure all LEDS are off
    clear_leds()
    
    while True:
        Y, M, D, W, HH, MM, SS, MS = rtc.datetime() # Get current timestamp
        toggle_leds(HH, MM, SS) # Toggle LEDs on/off according to time

        now_time = f"{HH:0>2}:{MM:0>2}:{SS:0>2}" # Current RTC time (HH:MM:SS)
        sync_time = SYNC_TIMES['october' if (M == 10) else 'default'] # 01:00:01/02:00:01
        # Synchronise the RTC if sync time is reached
        if (now_time == sync_time):
            sync_rtc(rtc, blocking=False)

        time.sleep(1) # Wait 1 second
    
except KeyboardInterrupt:
    clear_leds()
    sys.exit(0)