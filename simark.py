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
dt_start = day[0]
dt_end = day[-1]
dt_timeofday = dt.timedelta(hours=hour)
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
c_dataobj = da.DataAccess('Yahoo')
df_close = c_dataobj.get_data(ldt_timestamps, ls_symbols, "close")
vals = np.random.randint(0, 1000, len(ls_symbols))
vals = vals / float(sum(vals))
vals = vals.reshape(1, -1)
df_alloc = pd.DataFrame(vals,
            index=[ldt_timestamps[0] + dt.timedelta(hours=5)],
            columns=ls_symbols)
dt_last_date = ldt_timestamps[0]
for dt_date in ldt_timestamps[1:]:
    if dt_last_date.month != dt_date.month:
        na_vals = np.random.randint(0, 1000, len(ls_symbols))
        na_vals = na_vals / float(sum(na_vals))
        na_vals = na_vals.reshape(1, -1)
        df_new_row = pd.DataFrame(na_vals, index=[dt_date],
                                    columns=ls_symbols)
        df_alloc = df_alloc.append(df_new_row)
    dt_last_date = dt_date
df_alloc['_CASH'] = 0.0
(ts_funds, ts_leverage, f_commission, f_slippage, f_borrow_cost) = qstksim.tradesim(df_alloc,
                df_close, f_start_cash=amt, i_leastcount=1, b_followleastcount=True,
                f_slippage=0.0005, f_minimumcommision=5.0, f_commision_share=0.0035,
                i_target_leverage=1, f_rate_borrow=3.5, log="transaction.csv")
print ts_funds, ts_leverage, f_commission, f_slippage, f_borrow_cost

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




f.close()




'''
http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_3
http://wiki.quantsoftware.org/index.php?title=QSTK_Tutorial_2
'''
