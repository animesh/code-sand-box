import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def simulate(dt_start, dt_end,ls_symbols ,ls_alloc ):
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    na_price = d_data['close'].values
    na_normalized_price = na_price / na_price[0, :]
    na_rets = na_normalized_price.copy()
    tsu.returnize0(na_rets)
    dret=d_data['open'].values-d_data['close'].values
    dvol=d_data['volume'].values
    cum_ret = np.mean(d_data['close'].values * (1 + d_data['close'].values))
    portfolio_daily_rets = np.dot(na_rets,ls_alloc) 
    k_sharpe=np.sqrt(252)
    pdr_mu=np.mean(portfolio_daily_rets)
    pdr_sig=np.std(portfolio_daily_rets)
    sharpe_ratio = k_sharpe*pdr_mu/pdr_sig
    na_port_total = np.cumprod(portfolio_daily_rets + 1)
    na_component_total = np.cumprod(portfolio_daily_rets + 1, axis=0)
    cum_ret = np.cumprod(na_port_total + 1, axis=0)
    return sharpe_ratio, pdr_sig, pdr_mu, na_port_total[-1]

maxsr=float("-inf")
maxalloc=""
c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
n=10
slist=  ['TLAB', 'CSCO', 'INTC', 'MSFT']
salloc = [1/float(len(slist)),1/float(len(slist)),1/float(len(slist)),1/float(len(slist))] 
sd=dt.datetime(2009, 1, 1)
se=dt.datetime(2011, 12, 31)
print simulate(sd,se, slist,salloc)
for i in range(n):
    for j in range(n):
        for k in range(n):
            if 1-((i+j+k)/float(n))>=0:
                print i/float(n), j/float(n), k/float(n), 1-((i+j+k)/float(n))
                salloc=[round(i/float(n),2), round(j/float(n),2), round(k/float(n),2), round(1-((i+j+k)/float(n)),2)]
                sr,sig,mu,cr=simulate(sd,se,slist ,salloc)
                if sr>maxsr:
                    maxsr=sr
                    maxalloc=salloc
print i,j,k,slist,salloc,sd,se, sr,sig,mu,cr, maxalloc,maxsr

'''
slist=  ['BRCM', 'TXN', 'AMD', 'ADI']  
salloc= [0,0,0,1]
sd=dt.datetime(2010, 1, 1)
se=dt.datetime(2010, 12, 31)
print simulate(sd,se, slist,salloc)
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
