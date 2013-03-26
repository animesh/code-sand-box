'''
http://wiki.quantsoftware.org/index.php?title=QSTK_License
http://wiki.quantsoftware.org/index.php?title=QSTK_Tutorial_1#Prerequisites
http://wiki.quantsoftware.org/index.php?title=CompInvestI_Homework_1
https://code.google.com/p/code-sand-box/source/list
https://code.google.com/hosting/settings
https://class.coursera.org/compinvesting1-002/quiz/start?quiz_id=188
https://piazza.com/class#spring2013/1/606
https://www.coursera.org/user/i/185bb8b16b9f8734c33cb05b6484de4b
'''

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd



def main():

    ls_symbols = ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]
    dt_start = dt.datetime(2006, 1, 1)
    dt_end = dt.datetime(2010, 12, 31)
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    na_price = d_data['close'].values
    plt.clf()
    plt.plot(ldt_timestamps, na_price)
    plt.legend(ls_symbols)
    plt.ylabel('Adjusted Close')
    plt.xlabel('Date')
    plt.show()
    
    
if __name__ == '__main__':
    main()
