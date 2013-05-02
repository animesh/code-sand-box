from pyeeg import *
from numpy.random import randn
from matplotlib.pyplot import *

with open("eegsigfrg.txt") as input:
    sig = zip(*(line.strip().split('\t') for line in input))
ls = [map(int, x) for x in sig]
#print hurst(ls[:][1])
print ls

# FFT

C = abs(fft(zip(*ls)[1]))
B = [0.5,4,7,12,30] # d,t,a,b,g
F = 512

spectrum =zeros(len(B)-1);
for i in xrange(0,len(B)-1):
        Freq = float(B[i])                                                                          ## Xin Liu
        Next_Freq = float(B[i+1])
        spectrum[i] = sum(C[floor(Freq/F*len(C)):floor(Next_Freq/F*len(C))])
relative_spectrum = spectrum/sum(spectrum)

# plot histogram
subplot( 2, 1, 1 ) # r,c,f
plot(zip(*ls)[1],'ro-',B,'b.')
subplot( 2, 1, 2 ) 
hist(relative_spectrum)
show()

# first order

D=[]
for i in xrange(1,len(abs(fft(zip(*ls)[1])))):
        D.append(abs(fft(zip(*ls)[1]))[i]-abs(fft(zip(*ls)[1]))[i-1])
#print D

# EI

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
http://en.wikipedia.org/wiki/Neural_oscillation
http://hive-eu.org/
http://www.scholarpedia.org/article/Models_of_epilepsy
http://cs.smith.edu/dftwiki/index.php/MatPlotLib_Tutorial_1
http://code.google.com/p/labstreaminglayer/
http://opus.kobv.de/tuberlin/volltexte/2012/3377/pdf/haufe_stefan.pdf
'''
