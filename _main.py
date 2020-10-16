from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5

# MetaTrader 5に接続する
if not mt5.initialize():
   print("initialize() failed")
   mt5.shutdown()
 
# # 接続状態とパラメータをリクエストする
# print('terminal_info >>>>>>>>>')
# print(mt5.terminal_info())
# # MetaTrader 5バージョンについてのデータを取得する
# print('version >>>>>>>>>')
# print(mt5.version())
 
audusd_ticks = mt5.copy_ticks_range("AUDUSD", datetime(2020,1,27,13), datetime(2020,1,28,13), mt5.COPY_TICKS_ALL)
 
# タイムゾーンを使用するためのpytzモジュールをインポートする
import pytz
# タイムゾーンをUTCに設定する
timezone = pytz.timezone("Etc/UTC")
utc_from = datetime(2020, 1, 10, tzinfo=timezone)
utc_to = datetime(2020, 1, 11, hour = 13, tzinfo=timezone)
# audusd_rates = mt5.copy_rates_range("AUDUSD", mt5.TIMEFRAME_M5, utc_from, utc_to)
audusd_rates = mt5.copy_rates_range("AUDUSD", mt5.TIMEFRAME_M5, datetime(2019, 12, 10, 13), datetime(2020, 1, 11, 13))
 
# MetaTrader 5への接続をシャットダウンする
mt5.shutdown()
 
# PLOT
# 取得したデータからDataFrameを作成する
df = pd.DataFrame(audusd_rates)

# smaのデータを作成
from models import sma

sma25Inst = sma.sma(25)
df['sma25'] = sma25Inst.generateSmaColumnSeries(df['close'])

sma50Inst = sma.sma(50)
df['sma50'] = sma50Inst.generateSmaColumnSeries(df['close'])

sma75Inst = sma.sma(75)
df['sma75'] = sma75Inst.generateSmaColumnSeries(df['close'])

sma100Inst = sma.sma(100)
df['sma100'] = sma100Inst.generateSmaColumnSeries(df['close'])

sma200Inst = sma.sma(200)
df['sma200'] = sma200Inst.generateSmaColumnSeries(df['close'])

# 秒での時間をdatetime形式に変換する
df['time'] = pd.to_datetime(df['time'], unit='s')

export_path = 'exports/' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.csv'
df.to_csv(export_path)

print('df.head() >>>>>>>>>')
print(df.head(300))

# チャートにティックを表示する
plt.plot(df['time'], df['close'], 'r-', label='close')
 
# 凡例を表示する
plt.legend(loc='upper left')
 
# ヘッダを追加する
plt.title('AUDUSD close')
 
# チャートを表示する
plt.show()