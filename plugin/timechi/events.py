#!/usr/bin/env python

# Event = callable accepting Timer instance
# TODO: Count characters entered / movements / rename Timer? / ideas? :he event

def i_mode_entered(timer):
    busy(timer)

def i_mode_left(timer):
    busy(timer)

# Basic events

def busy(timer):
    timer.resume()

def idle(timer):
    timer.stop()

def save(timer):
    # FIXME
    timer.stop()
    print "[*] timechi saving progress"
    report = open("progress.txt", "a+")
    report.write("%s\n" % timer.state)
    report.close()
