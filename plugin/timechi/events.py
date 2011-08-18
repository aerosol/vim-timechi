#!/usr/bin/env python

#import time
from timechi.utils import log

# Event = callable accepting session instance
# TODO: Count characters entered / movements / ideas? :he event

def i_mode_entered(session):
    ping(session)

def i_mode_left(session):
    ping(session)

# Basic events

def ping(session):
    session.resume()

def idle(session):
    session.inc('total_time', session.pause())

def save(session):
    total_time = session.inc('total_time', session.pause())
    saves = session.inc('saves')
    log("Total time: %s with %s saves" % (total_time, saves))


