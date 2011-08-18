#!/usr/bin/env python

#import time
from timechi.utils import log
from timechi.achievements import achievement

# Event = callable accepting session instance
# TODO: Count characters entered / movements / ideas? :he event

def i_mode_entered(session):
    return ping(session)

def i_mode_left(session):
    return ping(session)

# Basic events

def ping(session):
    return session.resume()

def idle(session):
    return session.inc('total_time', session.pause())

@achievement
def save(session):
    total_time = session.inc('total_time', session.pause())
    saves = session.inc('save')
    log("Total time: %s with %s saves" % (total_time, saves))
    return saves


