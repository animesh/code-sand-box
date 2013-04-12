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
f = open(otp, 'w')


data = np.loadtxt(inp, delimiter=',',
            dtype={'names': ('year', 'month','day','ticker','action','number'),
                'formats': ('I2','I1','I1','S6','S4','I2')})
sym = data['ticker']
vol = data['number']  
day = []
hour = 16
for i in range(len(data)):
    day.append(dt.datetime(data['year'][i],data['month'][i],data['day'][i],hour))
    f.write("%s,%d\n" % (day[i],amt))

ls_symbols = list(set(sym))
ldt_timestamps = du.getNYSEdays(day[0], day[-1], dt.timedelta(hours=hour))
c_dataobj = da.DataAccess('Yahoo')
df_close = c_dataobj.get_data(ldt_timestamps, ls_symbols, "close")

exist={}
exist[day[0]] = exist.get(day[0], 0) + 0

for sn in range(len(data)):
    if sn==0 and exist[day[0]]<1:
        exist[day[sn]] = exist.get(day[sn], 0) + 1
        vals = np.zeros(len(ls_symbols))
        for stk in range(len(ls_symbols)):
            if sym[0]==ls_symbols[stk]:
                vals[stk]+=vol[0]
        vals = vals.reshape(1, -1)
        df_alloc = pd.DataFrame(vals,
                    index=[day[0]],
                    columns=ls_symbols)
        print df_alloc
    elif exist[day[sn]]<1:
        exist[day[sn]] = exist.get(day[sn], 0) + 1
        vals = np.zeros(len(ls_symbols)) #df_alloc(day[sn-1]).values
        for stk in range(len(ls_symbols)):
            vals[stk]+=vol[sn]
        vals = vals.reshape(1, -1)
        df_new_row = pd.DataFrame(vals, index=[day[sn]],columns=ls_symbols)
        df_alloc = df_alloc.append(df_new_row)
    else:
        exist[dt_action] = exist.get(dt_action, 0) + 0
        print sn

                
#print dt_date,ii,df_alloc.ix[ii-1]#,df_alloc.ix[df_alloc.index[ii]]
print df_alloc
df_alloc['_CASH'] = 0.0
(ts_funds, ts_leverage, f_commission, f_slippage, f_borrow_cost) = qstksim.tradesim(df_alloc,
                df_close, f_start_cash=amt, i_leastcount=1, b_followleastcount=True,
                f_slippage=0.0005, f_minimumcommision=5.0, f_commision_share=0.0035,
                i_target_leverage=1, f_rate_borrow=3.5, log="transaction.csv")
#print ts_funds #, ts_leverage, f_commission, f_slippage, f_borrow_cost



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

#print df_close, df_alloc
#print df_close, na_price

f.close()


'''
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_3
http://wiki.quantsoftware.org/index.php?title=QSTK_Tutorial_2
http://stackoverflow.com/questions/9877391/how-to-get-the-closest-single-row-after-a-specific-datetime-index-using-python-p
'''
