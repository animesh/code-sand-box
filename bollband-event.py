import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import QSTK.qstksim as qstksim
import QSTK.qstkstudy.EventProfiler as ep
import datetime as dt
import pandas as pa
import numpy as np
#from matplotlib.pyplot import *
import math
import copy

def boll_band(sym,sd,ed):
    pd = 20
    inc = 1
    ts = du.getNYSEdays(sd,ed,dt.timedelta(hours=16))
    dobj = da.DataAccess('Yahoo')
    cp = dobj.get_data(ts, sym, "close")

    for i in range(pd-inc,len(cp)):
        bollval = (cp.values[i] - np.mean(cp.values[i-pd+inc:i+inc])) / (np.std(cp.values[i-pd+inc:i+inc]))
        return bollval 

def find_events(ls_symbols, d_data):

    df_close = d_data['actual_close']
    ts_market = df_close['SPY']
    print "Finding Events"
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            if i>20:
                start2 = ldt_timestamps[i-20]
                end2 = ldt_timestamps[i-1]
                start1 = ldt_timestamps[i-19]
                end1 = ldt_timestamps[i]
                f_symbb_today = boll_band([s_sym],start1,end1)
                f_symbb_yest = boll_band([s_sym],start2,end2)
                f_SPYbb_today = ts_market.ix[ldt_timestamps[i]]
                print f_symbb_today,f_symbb_yest,f_SPYbb_today
                if f_symbb_today <= -2.0 and f_symbb_yest > -2.0 and f_SPYbb_today >= 1.0:
                    df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events



if __name__ == '__main__':

    dt_start = dt.datetime(2007, 1, 1)
    dt_end = dt.datetime(2007, 2, 10)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    #ls_symbols = ['GOOG','IBM']
    ls_symbols.append('SPY')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)


    df_events = find_events(ls_symbols, d_data)
    print "Creating Study"
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename='MyEventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')



'''
http://cran.r-project.org/doc/contrib/Fox-Companion/appendix-mixed-models.pdf
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_5
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_6
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_7
'''
