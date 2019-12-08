from time import sleep
import RPi.GPIO as GPIO
import argparse

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIOS = [20]


def setup(gpios):
    for gpio in gpios:
        GPIO.setup(gpio, GPIO.IN)


def read(pin):
    print ("Reading {}".format(pin))
    print (GPIO.input(pin))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Moisture sensor commands.')
    args = parser.parse_args()

    setup(GPIOS)

    while True:
        read(GPIOS[0])
        sleep(1)
