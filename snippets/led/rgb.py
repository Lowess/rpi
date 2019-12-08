from time import sleep
import RPi.GPIO as GPIO
import argparse

from enum import Enum

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class PrimaryColor(Enum):
    '''
        Defines which Gpio is mapped to which RGB Led pin
    '''
    __order__ = 'RED GREEN BLUE'
    RED = 16
    GREEN = 20
    BLUE = 21

    @staticmethod
    def list():
        return list(map(lambda c: c.value, PrimaryColor))


class Color(Enum):
    '''
        Defines combinations of colors to get secondary colors
    '''
    __order__ = 'RED GREEN BLUE YELLOW MAGENTA CYAN WHITE'

    RED = [PrimaryColor.RED]
    GREEN = [PrimaryColor.GREEN]
    BLUE = [PrimaryColor.BLUE]
    YELLOW = [PrimaryColor.RED, PrimaryColor.GREEN]
    MAGENTA = [PrimaryColor.RED, PrimaryColor.BLUE]
    CYAN = [PrimaryColor.BLUE, PrimaryColor.GREEN]
    WHITE = [PrimaryColor.BLUE, PrimaryColor.GREEN, PrimaryColor.RED]

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Color))

    @staticmethod
    def from_string(s):
        try:
            return Color[s]
        except KeyError:
            raise ValueError()


def setup(gpios):
    for gpio in gpios:
        print("Setup {} gpio".format(gpio))
        GPIO.setup(gpio, GPIO.OUT)


def reset():
    for pin in Color.WHITE.value:
        off(pin.value)


def blink(pin):
    print ("Blink {} led".format(pin))
    GPIO.output(pin, not GPIO.input(pin))


def off(pin):
    print ("Off {}".format(pin))
    GPIO.output(pin, GPIO.LOW)


def on(pin):
    print ("On {}".format(pin))
    GPIO.output(pin, GPIO.HIGH)


def parse_args():
    parser = argparse.ArgumentParser(description='Led commands.')

    parser.add_argument('cmd', type=str, help='Command to execute on the RGB Led',
                        choices=['on', 'off', 'blink'], default='on', nargs='?')

    parser.add_argument('color', type=Color.from_string, help='Color',
                        choices=list(Color), default=Color.WHITE, nargs='?')

    parser.add_argument('--sleep', dest='sleep', type=float, default=1)

    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()

    # Set GPIOs as output
    setup(PrimaryColor.list())

    # Switch off all pins
    reset()

    if args.cmd == "on":
        for pin in args.color.value:
            on(pin.value)

    elif args.cmd == "blink":
        while True:
            for color in Color.list():
                for pin in color:
                    blink(pin.value)
                sleep(args.sleep)

                reset()
