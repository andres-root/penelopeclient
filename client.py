from __future__ import print_function

from Adafruit_Thermal import *
import HTMLParser
import json
import os
import requests
import RPi.GPIO as IO
import time
from unidecode import unidecode


consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
# TODO: Add URL to env variables
url = os.environ['URL']
welcome_message = os.environ['WELCOME_MESSAGE']

# Initialize printer
printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)


def setup():
    # LED configuration
    IO.setmode(IO.BOARD)
    IO.setup(33, IO.OUT)
    IO.setup(31, IO.OUT)
    IO.setup(29, IO.OUT)

    # Print welcome message
    printer.print(unidecode(
            HTMLParser.HTMLParser().unescape(welcome_message)
        )
    )


def get_tweet():
    IO.output(33, True)
    time.sleep(1)
    tweet = json.loads(requests.get(url))
    IO.output(33, False)
    return tweet


def start_printing(tweet):
    '''
    TODO: Implement JSON parse
    '''
    # Printer LED on
    IO.output(31, True)
    time.sleep(1)

    # Start printing
    printer.inverseOn()
    printer.print(' ' + '{:<31}'.format(tweet['user_name']))
    printer.inverseOff()

    printer.underlineOn()
    printer.print('{:<32}'.format(tweet['date']))
    printer.underlineOff()

    # Remove HTML escape sequences
    # and remap Unicode values to nearest ASCII equivalents
    printer.print(unidecode(
            HTMLParser.HTMLParser().unescape(tweet['text'])
        )
    )

    printer.feed(3)

    # Printer LED off
    IO.output(31, False)

    time.sleep(5)

    IO.output(29, True)
    time.sleep(3)
    IO.output(29, False)

    IO.cleanup()

while True:
    setup()
    tweet = get_tweet()
    print(tweet)
    # start_printing(tweet)
    # IO.cleanup()
