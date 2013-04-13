import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
dahead=5


def find_events(ls_symbols, d_data):

    df_close = d_data['actual_close']
    ts_market = df_close['SPY']
    print "Finding Events"
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)-dahead):
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
            if f_symprice_today<6 and f_symprice_yest>=6:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1
                f.write("%s,%s,%s,%s,Buy,100\n" %
                        (ldt_timestamps[i].year,ldt_timestamps[i].month,ldt_timestamps[i].day,s_sym))
                f.write("%s,%s,%s,%s,Sell,100\n" %
                        (ldt_timestamps[i+dahead].year,ldt_timestamps[i+dahead].month,ldt_timestamps[i+5].day,s_sym))

    return df_events

if __name__ == '__main__':

    otp='action.csv'
    f = open(otp, 'w')

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

    print df_events

    f.close()

"""
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_4
http://wiki.quantsoftware.org/index.php?title=QSTK_Tutorial_9
http://wiki.quantsoftware.org/index.php?title=CompInvestI_Homework_2
https://class.coursera.org/compinvesting1-002/wiki/view?page=Week4
https://class.coursera.org/compinvesting1-002/quiz/index
https://code.google.com/hosting/settings
"""
