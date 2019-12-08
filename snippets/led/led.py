from time import sleep
import RPi.GPIO as GPIO
import argparse

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIOS = [16, 20, 21]


def setup(gpios):
    for gpio in gpios:
        GPIO.setup(gpio, GPIO.OUT)


def blink(pin, wait=0.1):
    print ("Blink {} led".format(pin))
    GPIO.output(pin, not GPIO.input(pin))
    sleep(wait)


def off(pin):
    print ("Off {}".format(pin))
    GPIO.output(pin, GPIO.LOW)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Led commands.')
    parser.add_argument('cmd', type=str, help='Cmd')
    parser.add_argument('--sleep', dest='sleep', type=float, default=0.1)
    args = parser.parse_args()

    setup(GPIOS)

    if args.cmd == "off":
        for gpio in GPIOS:
            off(gpio)

    elif args.cmd == "blink":
        while True:
            for gpio in GPIOS:
                blink(gpio, args.sleep)
