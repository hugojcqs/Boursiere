from django import template
import random
import math
from random import *
# make custom filter for django template

register = template.Library()

def rcolors(value):
    #return "#"+"%06x" % random.randint(0, 0xFFFFFF)
    letters = 'B,C,D,E,F'.split(',');
    color = '#';
    for i in range(6):
        color += letters[math.floor(random() * len(letters))]
    return color;
register.filter('rcolors', rcolors)
