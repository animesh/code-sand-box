import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def simulate(dt_start, dt_end,ls_symbols ,salloc ):
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    na_price = d_data['close'].values
    na_normalized_price = na_price / na_price[0, :]
    na_rets = na_normalized_price.copy()
    #print tsu.returnize0(na_rets)
    #plt.clf()
    #plt.plot(ldt_timestamps, na_normalized_price)
    #plt.legend(ls_symbols)
    #plt.ylabel('Adjusted Close')
    #plt.xlabel('Date')
    #plt.show()
    #plt.scatter(na_rets[:, 3], na_rets[:, 1], c='blue')
    dret=d_data['open'].values-d_data['close'].values
    dvol=d_data['volume'].values
    cum_ret = np.mean(d_data['close'].values * (1 + d_data['close'].values))
    k_sharpe=np.sqrt(252)
    dr_mean=np.mean(d_data['close'].values/d_data['open'].values-1)
    dr_sd=np.std(d_data['close'].values/d_data['open'].values-1)
    sharpe_ratio = k_sharpe*dr_mean/dr_sd
    #portfolio_daily_rets = 0.75 * GLD_daily_rets + 0.25 * SPY_daily_rets
    return dvol, dret, sharpe_ratio, cum_ret 
    
slist=['AAPL','GLD','GOOG','XOM']
salloc=[0.4, 0.4, 0.0, 0.2]
sd=dt.datetime(2011, 1, 1)
se=dt.datetime(2011, 12, 31)
vol, daily_ret, sharpe, cum_ret = simulate(sd,se,slist ,salloc)
print sharpe, np.mean(vol), cum_ret, daily_ret

'''
http://wiki.quantsoftware.org/index.php?title=QSTK_License
http://wiki.quantsoftware.org/index.php?title=QSTK_Tutorial_1#Prerequisites
http://wiki.quantsoftware.org/index.php?title=QuantSoftware_ToolKit#Documentation
http://wiki.quantsoftware.org/index.php?title=CompInvestI_Homework_1
https://code.google.com/p/code-sand-box/source/list
https://code.google.com/hosting/settings
https://class.coursera.org/compinvesting1-002/quiz/start?quiz_id=188
https://piazza.com/class#spring2013/1/606
https://www.coursera.org/user/i/185bb8b16b9f8734c33cb05b6484de4b
'''
