from pyeeg import *
from numpy.random import randn

a = randn(4096)
print a
#print hurst(a)
spectrum, relative_spectrum = bin_power(a, [0.5,4,7,12,30],512)
print spectrum, relative_spectrum


'''
http://pyeeg.org
https://github.com/akloster/python-mindwave
'''
