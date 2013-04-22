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

def find_events(ls_symbols, d_data):

    df_close = d_data['actual_close']
    ts_market = df_close['SPY']
    print "Finding Events"
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
            if f_symprice_today > f_symprice_yest:
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


    sym = ['GOOG']
    sym = ['AAPL']
    sym = ['IBM']
    sym = ['MSFT']
    sym = ['SPY']

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
http://cran.r-project.org/doc/contrib/Fox-Companion/appendix-mixed-models.pdf
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_5
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_6
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_7
'''
