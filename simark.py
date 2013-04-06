import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import pandas as pd
import numpy as np

amt=1000000
inp='orders2.csv'
otp='values.csv'
f = open(otp, 'w')

data = np.loadtxt(inp, delimiter=',',
            dtype={'names': ('year', 'month','day','ticker','action','number'),
                'formats': ('I2','I1','I1','S6','S4','I2')})
sym = data['ticker']
vol = data['number']  
day = []
for i in range(len(data)):
    day.append(dt.date(data['year'][i],data['month'][i],
                                  data['day'][i]))
    f.write("%s,%d\n" % (day[i],amt))
    
print sym,vol,day

f.close()

'''
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_3
http://wiki.quantsoftware.org/index.php?title=QSTK_Tutorial_2
'''
