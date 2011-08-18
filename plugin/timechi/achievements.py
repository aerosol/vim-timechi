#!/usr/bin/env python
import time
import subprocess
#import platform
from timechi.helpers import log

try:
    import vim
    say_command = vim.eval("g:timechi_notification_command")
except ImportError:
    say_command = "echo %s"

ACHIEVEMENTS = { 
            'save': [
                    (lambda x: int(x) == 1,
                        'Act like a pro'),
                    (lambda x: int(x) == 10,
                        'Act like a pro'),
                    (lambda x: int(x) == 15,
                        'Act like a pro'),
                    (lambda x: int(x) == 50,
                        'Animality!'),
                    (lambda x: int(x) == 100,
                        'Violence'),
                    (lambda x: int(x) == 500,
                        '500 Cent'),
                    (lambda x: int(x) == 1024,
                        'Kilosave'),
                    (lambda x: int(x) == 10000,
                        'Professional rapist'),
                    (lambda x: int(x) == 1000000,
                        'You should be a millionare by now'),
                    (lambda x: int(x) == 10000000,
                        'Mission impossible'),
                    ]}

def notify(session, achievements):
    for (_fn, achievement) in achievements:
        print "Timechi achievement unlocked: %s" % achievement
        cmd = say_command % achievement
        subprocess.Popen(cmd.split(" "))
        session.append('achievements', achievement)
        time.sleep(1)

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
            if achievements:
                notify(session, achievements)
            return result
    return wrapped


