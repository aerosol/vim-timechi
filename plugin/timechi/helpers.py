#!/bin/env python

DEBUG = False
try:
    import vim
    try:
        DEBUG = bool(vim.eval("g:timechi_debug"))
    except:
        DEBUG = False
except ImportError:
    print "Couldnt import vim - debug mode"
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
