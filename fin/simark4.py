import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import QSTK.qstksim as qstksim
import datetime as dt
import pandas as pd
import numpy as np

amt=1000000
inp='orders2.csv'
otp='values.csv'

data = np.loadtxt(inp, delimiter=',',
            dtype={'names': ('year', 'month','day','ticker','action','number'),
                'formats': ('I2','I1','I1','S6','S4','I2')})
sym = data['ticker']
vol = data['number']
act = data['action']
day = []
hour = 16
for i in range(len(data)):
    day.append(dt.datetime(data['year'][i],data['month'][i],data['day'][i],hour))

ls_symbols = list(set(sym))
#ls_symbols.append('_CASH')
dt_timeofday = dt.timedelta(hours=hour)
ldt_timestamps = du.getNYSEdays(day[0], day[-1], dt_timeofday)
c_dataobj = da.DataAccess('Yahoo')
df_close = c_dataobj.get_data(ldt_timestamps, ls_symbols, "close")


exist={}
for sn in range(len(data)):
    exist[day[sn]] = exist.get(day[sn], 0) + 0
    dt_action=day[sn]
    if sn>1:
        na_old = df_alloc.xs(day[sn-1]).values
        print sn, na_old
        if exist[dt_action]<1:
            exist[dt_action] = exist.get(dt_action, 0) + 1
            na_vals=na_old
            for stk in range(len(ls_symbols)):
                if sym[sn]==ls_symbols[stk] and act[sn]=="Buy":
                   na_vals[stk]+=vol[sn]
                if sym[sn]==ls_symbols[stk] and act[sn]=="Sell":
                   na_vals[stk]-=vol[sn]
            na_vals = na_vals.reshape(1, -1)
            df_new_row = pd.DataFrame(na_vals, index=[dt_action],columns=ls_symbols)
            df_alloc = df_alloc.append(df_new_row)
            na_old=na_vals
        else:
            exist[dt_action] = exist.get(dt_action, 0) + 1
            print exist[dt_action], df_alloc.index.searchsorted(dt_action) , "already present!", dt_action #,df_alloc.date
            na_vals = df_alloc.xs(dt_action).values
            print na_vals
            for stk in range(len(ls_symbols)):
                if sym[sn]==ls_symbols[stk] and act[sn]=="Buy":
                    df_alloc.xs(dt_action,copy=False)[sym[sn]]+=vol[sn]
                if sym[sn]==ls_symbols[stk] and act[sn]=="Sell":
                    df_alloc.xs(dt_action,copy=False)[sym[sn]]-=vol[sn]
            na_vals = df_alloc.xs(dt_action).values
            na_old=na_vals
            print na_old
    elif sn==1:
        na_old = df_alloc.xs(day[0] + dt.timedelta(hours=5)).values
        print sn, na_old
        if exist[dt_action]<1:
            exist[dt_action] = exist.get(dt_action, 0) + 1
            na_vals=na_old
            for stk in range(len(ls_symbols)):
                if sym[sn]==ls_symbols[stk] and act[sn]=="Buy":
                   na_vals[stk]+=vol[sn]
                if sym[sn]==ls_symbols[stk] and act[sn]=="Sell":
                   na_vals[stk]-=vol[sn]
            na_vals = na_vals.reshape(1, -1)
            df_new_row = pd.DataFrame(na_vals, index=[dt_action],columns=ls_symbols)
            df_alloc = df_alloc.append(df_new_row)
            na_old=na_vals
        else:
            exist[dt_action] = exist.get(dt_action, 0) + 1
            print exist[dt_action], df_alloc.index.searchsorted(dt_action) , "already present!", dt_action #,df_alloc.date
            na_vals = df_alloc.xs(dt_action).values
            print na_vals
            for stk in range(len(ls_symbols)):
                if sym[sn]==ls_symbols[stk] and act[sn]=="Buy":
                    df_alloc.xs(dt_action,copy=False)[sym[sn]]+=vol[sn]
                if sym[sn]==ls_symbols[stk] and act[sn]=="Sell":
                    df_alloc.xs(dt_action,copy=False)[sym[sn]]-=vol[sn]
            na_vals = df_alloc.xs(dt_action).values
            na_old=na_vals
            print na_old
    else:
        vals = np.zeros(len(ls_symbols))
        for stk in range(len(ls_symbols)):
            if sym[0]==ls_symbols[stk]:
                vals[stk]+=vol[0]
        vals = vals.reshape(1, -1)
        df_alloc = pd.DataFrame(vals,
                    index=[day[0] + dt.timedelta(hours=5)],
                    columns=ls_symbols)

        
                    
#print dt_date,ii,df_alloc.ix[ii-1]#,df_alloc.ix[df_alloc.index[ii]]

df_alloc = df_alloc / df_alloc.sum(axis=1)
df_alloc=df_alloc.fillna(method='ffill')
df_alloc=df_alloc.fillna(method='bfill')

print df_alloc

df_alloc['_CASH'] = 0.0
(ts_funds, ts_leverage, f_commission, f_slippage, f_borrow_cost) = qstksim.tradesim(df_alloc,
                df_close, f_start_cash=amt, i_leastcount=1, b_followleastcount=True,
                f_slippage=0.0005, f_minimumcommision=5.0, f_commision_share=0.0035,
                i_target_leverage=1, f_rate_borrow=3.5, log=otp)
print ts_funds #, ts_leverage, f_commission, f_slippage, f_borrow_cost



ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
d_data = dict(zip(ls_keys, ldf_data))
na_price = d_data['close'].values
na_normalized_price = na_price / na_price[0, :]
na_rets = na_normalized_price.copy()
tsu.returnize0(na_rets)
portfolio_daily_rets = np.dot(na_rets,1) 
k_sharpe=np.sqrt(252)
pdr_mu=np.mean(portfolio_daily_rets)
pdr_sig=np.std(portfolio_daily_rets)
sharpe_ratio = k_sharpe*pdr_mu/pdr_sig
na_port_total = np.cumprod(portfolio_daily_rets + 1)
na_component_total = np.cumprod(portfolio_daily_rets + 1, axis=0)
cum_ret = np.cumprod(na_port_total + 1, axis=0)
print sharpe_ratio, pdr_sig, pdr_mu, na_port_total[-1]


'''
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_3
http://wiki.quantsoftware.org/index.php?title=QSTK_Tutorial_2
http://stackoverflow.com/questions/9877391/how-to-get-the-closest-single-row-after-a-specific-datetime-index-using-python-p
'''
