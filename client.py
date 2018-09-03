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
url = os.environ['URL']
title = os.environ['TITLE']
subtitle = os.environ['SUBTITLE']
author = os.environ['AUTHOR']

# Initialize printer
printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

# Print welcome message
printer.print(unidecode(
        HTMLParser.HTMLParser().unescape(title)
    )
)

printer.feed(1)

printer.print(unidecode(
        HTMLParser.HTMLParser().unescape(subtitle)
    )
)

printer.feed(1)

printer.print(unidecode(
        HTMLParser.HTMLParser().unescape(author)
    )
)

printer.feed(1)

printer.print(unidecode(
        HTMLParser.HTMLParser().unescape('2018')
    )
)

printer.feed(4)


IO.setmode(IO.BOARD)
IO.setup(29, IO.OUT)
IO.output(29, True)
time.sleep(2)
IO.output(29, False)
IO.cleanup()

def setup():
    # LED configuration
    IO.setmode(IO.BOARD)
    IO.setup(33, IO.OUT)
    IO.setup(31, IO.OUT)
    IO.setup(29, IO.OUT)

def get_tweet():
    IO.output(33, True)
    time.sleep(1)
    tweet = json.loads(requests.get(url).text)
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
    printer.print(' ' + '{:<31}'.format(tweet['user']))
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

    printer.feed(6)

    # Printer LED off
    IO.output(31, False)

    time.sleep(5)

    IO.output(29, True)
    time.sleep(1.5)
    IO.output(29, False)

    IO.cleanup()
    time.sleep(40)

while True:
    setup()
    tweet = get_tweet()
    start_printing(tweet)
