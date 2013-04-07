from pyeeg import *
from numpy.random import randn

with open("eegsigfrg.txt") as input:
    sig = zip(*(line.strip().split('\t') for line in input))
ls = [map(int, x) for x in sig]
print hurst(ls[:][1])

spectrum, relative_spectrum = bin_power((zip(*ls)[1]), [0.5,4,7,12,30],512) # d/g,t,a,b
print spectrum, relative_spectrum

ER=(relative_spectrum[3]+relative_spectrum[0])/(relative_spectrum[1]+relative_spectrum[2])
print ER

bias=randn()
Un=sum(ER-relative_spectrum[:]-bias)
print Un

EI=ER/Un
print EI


'''
https://code.google.com/p/code-sand-box/source/browse/eegsigfrg.txt
http://code.google.com/p/pyeeg/source/browse/pyeeg.py
https://github.com/akloster/python-mindwave/blob/master/feedback.py
https://code.google.com/p/code-sand-box/source/browse/nseega.py
https://code.google.com/p/misccb/source/browse/geteegfromns.m
http://stackoverflow.com/questions/11059390/parsing-a-tab-separated-file-in-python
http://stackoverflow.com/questions/1909619/python-list-to-integers/1909632#1909632
http://brain.oxfordjournals.org/content/131/7/1818
'''
