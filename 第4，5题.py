from jaqs_fxdayu.data.dataservice import LocalDataService
ds = LocalDataService()
from time import time
from jaqs_fxdayu.data.hf_dataview import HFDataView
import matplotlib.pyplot as plt
import mpl_finance as mpf
import seaborn
## 加freq参数

start = time()
path = r'./min_data/VnTrader_1Min_Db'
props = {'fields': 'open,high,low,close,volume','symbol': 'BTCUSDT:binance', 'freq': '4H',
         'start_date':20180601000000}

Time_dict = ds.bar_reader(path,props)

dv = HFDataView()
dv.create_init_dv(Time_dict.set_index(["trade_date","symbol"]))

def plot_chart(close,alpha,M):
    fig,(ax,ax1) = plt.subplots(2,1,sharex=True, figsize=(15,8))
    ax.grid(axis='both')
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(500))
    ax1.grid()
    ax1.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax1.yaxis.set_major_locator(plt.MultipleLocator(M))
    ax.plot(close)
    ax1.plot(alpha)
    plt.show()

def RankPct(df):
    return df.rank(axis= 1, pct=True)

psy_j = dv.add_formula("psy_j", "Ts_Sum(close>Delay(close,1),12)/12*100", add_data=True)
alpha1_plot = dv.get_ts('psy_j', date_type='datetime')
open = dv.get_ts('open', date_type='datetime')
close = dv.get_ts('close', date_type='datetime')
print('本指标是心理线指标，是研究投资者对股市涨跌产生心里波动对情绪指标，对股市短期走势对研判具有一定参考意义。\n'
      '现象：本指标分布与0-100之间，当标的价格上涨到一定对程度时，psy_j指标也随之下跌，代表应当买入，当标的价格下跌到一定程度时，psy_j随之上涨，代表买入')
plot_chart(open, alpha1_plot,5)

dv.add_formula("close_ret", "Return(close,1)", add_data=True)
SharpeRatio20 = dv.add_formula('SharpeRatio20_J', "(Ts_Mean(close_ret,20)*250-0.03)/StdDev(close_ret,20)/Sqrt(250)",add_data=True)
alpha2_plot = dv.get_ts('SharpeRatio20_J', date_type='datetime')
print('本指标是20日夏普比率，代表每承受一单位风险会产生多少到超额报酬。\n'
      '现象：本指标分布与-8到8之间，当指标在低点时超额收益低，可以作为买入信号，指标处于高点时，收益率较高，可以作为卖出信号')
plot_chart(close, alpha2_plot,1)