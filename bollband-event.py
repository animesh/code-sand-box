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

    df_close = d_data['close']
    ts_market = df_close['SPY']
    bbspy = (ts_market-pa.rolling_mean(ts_market, 20))/pa.rolling_std(ts_market, 20)
    print "Finding Events", bbspy
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        s = df_close[s_sym]
        bb = (s-pa.rolling_mean(s, 20))/pa.rolling_std(s, 20)
        #s = pa.Series([1,3,5,np.nan,6,8])
        #print s,s-pa.rolling_mean(s, 2)/pa.rolling_std(s, 2)
        for i in range(1, len(ldt_timestamps)):
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            f_symreturn_today = (f_symprice_today / f_symprice_yest)
            #start2 = ldt_timestamps[i-20]
            #end2 = ldt_timestamps[i-1]
            #start1 = ldt_timestamps[i-19]
            #end1 = ldt_timestamps[i]
            #f_symbb_today = boll_band([s_sym],start1,end1)
            #f_symbb_yest = boll_band([s_sym],start2,end2)
            f_symbb_today = bb.ix[ldt_timestamps[i]]
            f_symbb_yest = bb.ix[ldt_timestamps[i-1]]
            f_symbb_spy = bbspy.ix[ldt_timestamps[i]]
            #if f_symprice_today < 6 and f_symprice_yest >= 6 and f_symreturn_today < 1:
            if f_symbb_today < -2 and f_symbb_yest >= -2 and f_symbb_spy >= 1.3:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events

if __name__ == '__main__':

    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
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
http://pandas.pydata.org/pandas-docs/dev/10min.html
http://pandas.pydata.org/pandas-docs/dev/computation.html
http://pandas.pydata.org/pandas-docs/stable/timeseries.html
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_6
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_7
'''
