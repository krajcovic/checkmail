#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'krajcovic'

from imapclient import IMAPClient
import sys
import time
import getopt

import RPi.GPIO as GPIO

DEBUG = True

HOSTNAME = 'mail.nitrok.cz'
MAILBOX = 'INBOX'

NEWMAIL_OFFSET = 1   # my unread messages never goes to zero, yours might
MAIL_CHECK_FREQ = 60 # check mail every 60 seconds

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GREEN_LED = 18
RED_LED = 23
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED,GPIO.OUT)

def loop(username, password):
    server = IMAPClient(HOSTNAME, use_uid=True)
    print(username, password)
    server.login(username, password)

    if DEBUG:
        print('Logging in as ' + username)
        select_info = server.select_folder(MAILBOX)
        print('%d messages in INBOX' % select_info['EXISTS'])

    folder_status = server.folder_status(MAILBOX, 'UNSEEN')
    newmails = int(folder_status['UNSEEN'])

    if DEBUG:
        print("You have", newmails, "new emails!")

    if newmails > NEWMAIL_OFFSET:
        GPIO.output(GREEN_LED, True)
        GPIO.output(RED_LED, False)
    else:
        GPIO.output(GREEN_LED, False)
        GPIO.output(RED_LED, True)

    time.sleep(MAIL_CHECK_FREQ)

def main(argv):

    username = None
    password = None

    try:
        opts, args = getopt.getopt(argv, "hu:p:", ["user=", "pass="])
    except getopt.GetoptError:
        print(__file__, '-u <user> -p <password>' )
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(__file__, '-u <user> -p <password>')
            sys.exit()
        elif opt in ("-u", "--user"):
            username = arg
        elif opt in ("-p", "--pass"):
            password = arg

    if username is None:
        print(__file__, '-u <user> -p <password>' )
        sys.exit(2)

    try:
        print('Press Ctrl-C to quit.')
        while True:
            loop(username, password)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main(sys.argv[1:])
