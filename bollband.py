import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import QSTK.qstksim as qstksim
import datetime as dt
import pandas as pa
import numpy as np
#from matplotlib.pyplot import *


sym = ['GOOG']
sym = ['AAPL']
sym = ['IBM']
sym = ['MSFT']
sd = dt.datetime(2010,1,1)
ed = dt.datetime(2010,12,31)
pd = 20
inc = 1
ts = du.getNYSEdays(sd,ed,dt.timedelta(hours=16))
dobj = da.DataAccess('Yahoo')
cp = dobj.get_data(ts, sym, "close",verbose=True)

for i in range(pd-inc,len(cp)):
    bollval = (cp.values[i] - np.mean(cp.values[i-pd+inc:i+inc])) / (np.std(cp.values[i-pd+inc:i+inc]))
    print i,ts[i],cp.values[i],bollval #,cp.values[i-pd+inc:i+inc]
    
'''
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_5
'''
