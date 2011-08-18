#!/usr/bin/env python
import datetime

def forever_alone_check(*args, **kwargs):
    today = datetime.datetime.now()
    return today.hour > 19 and today.weekday() in (4,5)

def night_check(*args, **kwagrs):
    today = datetime.datetime.now()
    return today.hour > 1 and today.hour < 4


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
                    ],
            'buff_created': [
                    (lambda x: int(x) == 1,
                        'Buffy'),
                    (lambda x: int(x) == 1000,
                        'Bruce Buffer'),
                ],
            'i_mode_left': [
                    (lambda x: int(x) == 10,
                        'Hedonist'),
                    (lambda x: int(x) == 1000,
                        'Escapist'),
                    (lambda x: int(x) == 10000,
                        'Superinsecure'),
                    (lambda x: int(x) == 100000,
                        'Run Forrest Run')
                ],
            'ping': [
                    (forever_alone_check, 'Forever Alone'),
                    (night_check, 'Night owl'),
                ]

            }

