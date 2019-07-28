from django import template
import random
import math
from random import *
# make custom filter for django template

register = template.Library()
color_list = ['#',]

def rcolors(value):
    #return "#"+"%06x" % random.randint(0, 0xFFFFFF)
    letters = 'B,C,D,E,F'.split(',');
    color = '#';
    while color in color_list:
        for i in range(6):
            color += letters[math.floor(random() * len(letters))]
    color_list.append(color)
    return color;
register.filter('rcolors', rcolors)

def csplit(value):
    #return "#"+"%06x" % random.randint(0, 0xFFFFFF)
    letters = 'B,C,D,E,F'.split(',');
    color = '#';
    while color in color_list:
        for i in range(6):
            color += letters[math.floor(random() * len(letters))]
    color_list.append(color)
    return color;
register.filter('split', csplit)
