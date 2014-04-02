#!/usr/bin/env python

from types import *
from awesome_print import ap

objects = [
        ["abc\ndef", {(1,2) : (1,2,3,4,5,6,7,8,9,10,11)}],
        None,
        BooleanType,
        True,
        "Hello, World!",
        65535,
        3.1415926,
        (1,2,3,4,5,6,7,8,9,10,11),
        [1,2,3,4,5],
        {'one': 1, 'two': 2, 'ten': 10},
        {
            'one': 1,
            'two': ['uno', 'dos', 'tres'],
            'six': {
                'ein': 1,
                'zwei': 2,
                'drei': 3
            }
        }
        ]

print '>> from awesome_print import ap'
for object in objects:
    if type(object) is str:
        print '>> ap("' + str(object) +'")'
    else:
        print '>> ap(' + str(object) +')'
    ap(object)
