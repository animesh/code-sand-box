from pyeeg import *
from numpy.random import randn

a = randn(4096)
print a
#print hurst(a)
spectrum, relative_spectrum = bin_power(a, [0.5,4,7,12,30],512)
print spectrum, relative_spectrum



'''
http://code.google.com/p/pyeeg/source/browse/pyeeg.py
https://github.com/akloster/python-mindwave/blob/master/feedback.py
https://code.google.com/p/code-sand-box/source/browse/nseega.py
https://code.google.com/hosting/settings
'''
