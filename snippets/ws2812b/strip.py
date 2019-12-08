#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import PixelStrip, Color
import argparse

# LED strip configuration:
LED_COUNT = 74        # Number of LED pixels.
# LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def getPivot(strip):
    pivot = strip.numPixels() / 2
    if (pivot % 2) == 0:
        return pivot
    else:
        return pivot + 1

# Define functions which animate LEDs in various ways.
def biColorWipe(strip, color, pivot, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        if i < pivot:
            strip.setPixelColor(i, color)
        else:
            strip.setPixelColor(i, Color(255,255,255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


# def theaterChase(strip, color, wait_ms=50, iterations=10):
#     """Movie theater light style chaser animation."""
#     for j in range(iterations):
#         for q in range(3):
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i + q, color)
#             strip.show()
#             time.sleep(wait_ms / 1000.0)
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i + q, 0)


# def wheel(pos):
#     """Generate rainbow colors across 0-255 positions."""
#     if pos < 85:
#         return Color(pos * 3, 255 - pos * 3, 0)
#     elif pos < 170:
#         pos -= 85
#         return Color(255 - pos * 3, 0, pos * 3)
#     else:
#         pos -= 170
#         return Color(0, pos * 3, 255 - pos * 3)


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true',
                        help='clear the display on exit')
    parser.add_argument('-r', '--red', type=int, default=0,
                        help='Value fqor red color')
    parser.add_argument('-g', '--green', type=int, default=0,
                        help='Value for green color')
    parser.add_argument('-b', '--blue', type=int, default=0,
                        help='Value for blue color')
    parser.add_argument('-w', '--wait', type=int, default=50,
                        help='Value for wait')

    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ,
                       LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            pivot = getPivot(strip)
            print("Color wipe animations. pivot {}".format(pivot))
            biColorWipe(strip, Color(args.red, args.green,
                                     args.blue), pivot, args.wait)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
