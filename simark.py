import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import pandas as pd
import numpy as np


data = np.loadtxt('orders.csv', delimiter=',',
            dtype={'names': ('year', 'month','day','ticker','action','number'),
                'formats': ('f2','f2','f2','S5','S5','I2')})
sym = data['ticker']
vol = data['number']  
day = []
for i in range(0, len(data)):
    day.append(dt.date(data['year'].astype(int)[i],data['month'].astype(int)[i],
                                  data['day'].astype(int)[i]))

print sym,vol,day


'''
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_3
http://wiki.quantsoftware.org/index.php?title=QSTK_Tutorial_2
http://stackoverflow.com/questions/13752988/usecols-in-loadtxt
http://stackoverflow.com/questions/10873824/how-to-convert-2d-float-numpy-array-to-2d-int-numpy-array
'''
