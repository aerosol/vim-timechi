#!/usr/bin/env python
import time
import os
import uuid
import shelve

from timechi import events
from timechi.helpers import log, atomic, Singleton

def session():
    return Session()

class Session(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.session_id = uuid.uuid1()
        log("Initializing session %s" % self)
        self.started = time.time()
        self.paused = None
        self.resumed = None
        self.total = 0

    @property
    def state(self):
        log("Performing session state check")
        if self.paused:
            return self.total
        if self.resumed:
            return self.total + (time.time() - self.resumed)
        return time.time() - self.started

    def pause(self):
        if not self.paused:
            self.paused = time.time()
            self.total += self.paused - (self.resumed or self.started)
            self.resumed = None
            log("Session %s paused" % self)
        return self.total

    def resume(self):
        if not self.resumed:
            self.resumed = time.time()
            self.paused = None
            log("Session %s resumed" % self)
        return self.total

    def report_event(self, event):
        log("Event reported: %s" % event)
        event_fn = getattr(events, event, None)
        assert event_fn is not None and callable(event_fn), \
                "Event %s must be callable" % event
        return event_fn(self)

    @atomic
    def lookup(self, k, default=""):
        db = self.vault
        v = db.get(k, default)
        return (db, v)

    @atomic
    def append(self, k, v):
        db = self.vault
        li = db.get(k, [])
        li.append(v)
        db[k] = li
        return (db, li)

    @atomic
    def store(self, k, v):
        db = self.vault
        db[k] = v
        return (db, v)

    @atomic
    def inc(self, k, a=1):
        db = self.vault
        v = db.get(k, 0)
        db[k] = v + a
        result = db[k]
        return (db, result)

    @atomic
    def dec(self, k, a=1):
        db = self.vault
        v = db.get(k, 0)
        if v > 0:
            db[k] = (v - a)     
            result = db[k]
        return (db, result)

    @property
    def vault(self):
        home = os.getenv('USERPROFILE') or os.getenv('HOME')
        datadir = os.path.join(home, '.vimtimechi')
        vault = os.path.join(datadir, "vault.db")
        if not os.path.exists(vault):
            log("Ensuring DB is present at %s..." % datadir)
            if not os.path.exists(datadir):
                log("Creating datadir...")
                os.mkdir(datadir)
        return shelve.open(vault)

    def __str__(self):
        return str(self.session_id)

        

            


