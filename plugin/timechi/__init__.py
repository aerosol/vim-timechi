#!/usr/bin/env python
import time
from timechi import events

class Singleton(type):
    _instances = {}
    def __call__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__call__(*args, **kwargs)
        return class_._instances[class_]

def get_timer():
    return Timer()

class Timer(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.started = time.time()
        self.stopped = None
        self.total = 0

    @property
    def state(self):
        if self.stopped:
            return self.total
        return self.total + (time.time() - self.started)

    def stop(self):
        self.stopped = time.time()
        self.total += self.stopped - self.started
        print "[-] timechi stopped"

    def resume(self):
        if self.stopped:
            self.stopped = None
            self.started = time.time()
            print "[+] timechi resumed"

    def report_event(self, event):
        event_fn = getattr(events, event, None)
        assert event_fn is not None and callable(event_fn)
        return event_fn(self)


            


