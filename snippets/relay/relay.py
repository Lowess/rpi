import RPi.GPIO as GPIO
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

GPIOS = [17, 27, 22, 23]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


def setup(gpios):
    for gpio in gpios:
        GPIO.setup(gpio, GPIO.OUT)


@app.route('/')
def index():
    return 'API is up'


@app.route('/off/<int:pin>')
def off(pin):
    print("Off {}".format(pin))
    GPIO.output(pin, GPIO.HIGH)
    return 'ok'


@app.route('/on/<int:pin>')
def on(pin):
    print("On {}".format(pin))
    GPIO.output(pin, GPIO.LOW)
    return 'ok'


setup(GPIOS)
