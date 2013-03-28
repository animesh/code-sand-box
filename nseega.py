from pyeeg import *
from numpy.random import randn

with open("eegsigfrg.txt") as input:
    sig = zip(*(line.strip().split('\t') for line in input))
ls = [map(int, x) for x in sig]
print hurst(ls[:][1])
spectrum, relative_spectrum = bin_power((zip(*ls)[1]), [0.5,4,7,12,30],512)
print spectrum, relative_spectrum



'''
http://code.google.com/p/pyeeg/source/browse/pyeeg.py
https://github.com/akloster/python-mindwave/blob/master/feedback.py
https://code.google.com/p/code-sand-box/source/browse/nseega.py
https://code.google.com/p/misccb/source/browse/geteegfromns.m
https://code.google.com/hosting/settings
http://stackoverflow.com/questions/11059390/parsing-a-tab-separated-file-in-python
http://stackoverflow.com/questions/1909619/python-list-to-integers/1909632#1909632
'''
