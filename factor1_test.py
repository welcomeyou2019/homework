
from jaqs_fxdayu.research import TimingDigger
import warnings
from jaqs_fxdayu.data.dataservice import LocalDataService
from jaqs_fxdayu.data.hf_dataview import HFDataView
warnings.filterwarnings('ignore')
ds = LocalDataService()
path = r'./min_data/VnTrader_1Min_Db'
props = {'fields': 'open,high,low,close,volume','symbol':'EOSUSDT:binance','freq':"5Min",
         'start_date':20180801000000}  #起始时间是2018.08.01

Time_dict = ds.bar_reader(path,props)
dv1H = HFDataView()
dv1H.create_init_dv(Time_dict.dropna().set_index(["trade_date","symbol"]))
dv1H.add_formula("psy", "Ts_Sum(close>Delay(close,1),12)/12*100", add_data=True)
psy = dv1H.get_ts('psy')

#设置进出场信号
long = dv1H.add_formula('long','If(psy>=75,2,0)',add_data = True)
short = dv1H.add_formula('short','If(psy<75,-2,0)',add_data = True)
#出场信号
close_long = dv1H.add_formula('closeLong','If(long==-2,1,0)',add_data = True)
close_short = dv1H.add_formula('closeShort','If(short==2,-1,0)',add_data = True)

def TimingSignal(td, dv, long='long', short='short', closeLong='closeLong', closeShort='closeShort', mhp=None, sl=None,
                 sp=None):
    td.process_signal(
        sig_type='long',
        enter_signal=dv.get_ts(long),
        exit_signal=dv.get_ts(closeLong),
        price=dv.get_ts('close'),
        max_holding_period=mhp,
        stoploss=-sl,
        stopprofit=sp
    )

    td.process_signal(
        sig_type='short',
        enter_signal=dv.get_ts(short),
        exit_signal=dv.get_ts(closeShort),
        price=dv.get_ts('close'),
        max_holding_period=mhp,
        stoploss=-sl,
        stopprofit=sp
    )


psy = TimingDigger(output_folder='.', output_format='pdf', signal_name='psy')
TimingSignal(psy, dv1H,  mhp=100, sl=0.05, sp=0.3)

psy.create_event_report(sig_type="long")
psy.create_event_report(sig_type="short")
psy.create_event_report(sig_type="long_short")


