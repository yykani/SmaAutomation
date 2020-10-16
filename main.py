# Import common modules
from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
# import matplotlib.pyplot as plt
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()

# Connect to MetaTrader5
if not mt5.initialize():
   print("initialize() failed")
   mt5.shutdown()

# Set timezone as utc
import pytz
timezone = pytz.timezone("Etc/UTC")
utc_from = datetime(2020, 1, 10, tzinfo=timezone)
utc_to = datetime(2020, 1, 11, hour = 13, tzinfo=timezone)

# Instantiate product models
from models.product import product
gbpusd = product('GBPUSD', mt5.TIMEFRAME_M5, utc_from, utc_to)
eurusd = product('EURUSD', mt5.TIMEFRAME_M5, utc_from, utc_to)
audusd = product('AUDUSD', mt5.TIMEFRAME_M5, utc_from, utc_to)

# Get DataFrames of rates each currency pairs
products = [gbpusd, eurusd, audusd]
rates_dataframes = []
for product in products:
   rates_dataframes.append(product.getRatesDataFrame())

# Disconnect from MetaTrader5
mt5.shutdown()

# Create SMA data
from models.sma import sma

for df in rates_dataframes:
   sma25Inst = sma(25)
   df['sma25'] = sma25Inst.generateSmaData(df['close'])

   sma50Inst = sma(50)
   df['sma50'] = sma50Inst.generateSmaData(df['close'])

   sma75Inst = sma(75)
   df['sma75'] = sma75Inst.generateSmaData(df['close'])

   sma100Inst = sma(100)
   df['sma100'] = sma100Inst.generateSmaData(df['close'])

   sma200Inst = sma(200)
   df['sma200'] = sma200Inst.generateSmaData(df['close'])

   # 秒での時間をdatetime形式に変換する
   df['time'] = pd.to_datetime(df['time'], unit='s')

   export_path = 'exports/' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.csv'
   df.to_csv(export_path)

   print('df.head() >>>>>>>>>')
   print(df.head(300))

   # # チャートにティックを表示する
   # plt.plot(df['time'], df['close'], 'r-', label='close')
   
   # # 凡例を表示する
   # plt.legend(loc='upper left')
   
   # # ヘッダを追加する
   # plt.title('AUDUSD close')
   
   # # チャートを表示する
   # plt.show()