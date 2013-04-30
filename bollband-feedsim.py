import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import QSTK.qstksim as qstksim
import QSTK.qstkstudy.EventProfiler as ep
import datetime as dt
import pandas as pa
import numpy as np
import math
import copy


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
        for i in range(1, len(ldt_timestamps)):
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            f_symreturn_today = (f_symprice_today / f_symprice_yest)
            f_symbb_today = bb.ix[ldt_timestamps[i]]
            f_symbb_yest = bb.ix[ldt_timestamps[i-1]]
            f_symbb_spy = bbspy.ix[ldt_timestamps[i]]
            if f_symbb_today < -2 and f_symbb_yest >= -2 and f_symbb_spy >= 1:
                df_new_row = pa.DataFrame(100, index=ldt_timestamps[i],columns=[s_sym])
                df_alloc = df_alloc.append(df_new_row)
                
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
    
    print "Simulating Study"
    (ts_funds, ts_leverage, f_commission, f_slippage, f_borrow_cost) = qstksim.tradesim(df_alloc,
                df_close, f_start_cash=1000000, i_leastcount=1, b_followleastcount=True,
                f_slippage=0.0005, f_minimumcommision=5.0, f_commision_share=0.0035,
                i_target_leverage=1, f_rate_borrow=3.5, log='simbb.csv')


'''
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_7
'''
