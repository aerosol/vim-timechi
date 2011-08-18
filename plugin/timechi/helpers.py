#!/bin/env python
import subprocess
import time
from timechi.achievements import ACHIEVEMENTS
#import platform

DEBUG = False
try:
    import vim
    DEBUG = bool(vim.eval("g:timechi_debug"))
    notification_command = vim.eval("g:timechi_notification_command")
except ImportError:
    print "Couldnt import vim - debug mode"
    notification_command = "echo %s > /dev/null"
    DEBUG = True

if DEBUG:
    def log(msg):
        with open('/tmp/vimtimechi.log', 'a+') as f:
            f.write("%s\n" % msg)
else:
    log = lambda msg: DEBUG


def atomic(fn):
    """Poor man's transactions"""
    def wrapped(*args, **kwargs):
        (db, res) = fn(*args, **kwargs)
        log("Atomic operation %s%s: %s" \
            % (fn.__name__, args[1:], res))
        db.close()
        return res
    return wrapped


class Singleton(type):
    _instances = {}
    def __call__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__call__(*args, **kwargs)
        return class_._instances[class_]


def notify(session, achievements):
    for (_fn, achievement) in achievements:
        if achievement not in session.lookup('achievements', []):
            print "Timechi achievement unlocked: %s" % achievement
            cmd = notification_command % achievement
            subprocess.Popen(cmd.split(" "))
            session.append('achievements', achievement)
            time.sleep(1)
        else:
            log("Achievement %s already unlocked." % achievement)

def achievement(fn):
    """Poor man's events"""
    def wrapped(*args, **kwargs):
        event = fn.__name__
        log("Checking for achievements available: %s" % event)
        if not event in ACHIEVEMENTS.keys():
            return fn(*args, **kwargs)
        else:
            log("Evaluating achievement conditions")
            result = fn(*args, **kwargs)
            session = args[0]
            val = session.lookup(event) or "0"
            achievements = filter(lambda (fun, prize): \
                    fun(val), ACHIEVEMENTS[event])
            log("Achievements filtered %s" % achievements)
            notify(session, achievements)
            return result
    return wrapped


