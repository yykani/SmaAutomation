# Import common modules
import os
from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
# import matplotlib.pyplot as plt
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()

# Connect to MetaTrader5
if not mt5.initialize():
   mt5.shutdown()
   raise RuntimeError('initialize() failed')

# Set timezone as utc
import pytz
timezone = pytz.timezone("Etc/UTC")
utc_from = datetime(2015, 10, 1, tzinfo=timezone)
utc_to = datetime(2020, 10, 1, hour = 13, tzinfo=timezone)

# Instantiate Products
from models.product import Product
gbpusd = Product('GBPUSD', mt5.TIMEFRAME_M5, utc_from, utc_to)
eurusd = Product('EURUSD', mt5.TIMEFRAME_M5, utc_from, utc_to)
audusd = Product('AUDUSD', mt5.TIMEFRAME_M5, utc_from, utc_to)

# Get DataFrames of rates each currency pairs
products = [gbpusd, eurusd, audusd]
for product in products:
   product.set_rates_dataframe()

# Disconnect from MetaTrader5
mt5.shutdown()

# Create a new directory to save csv  
new_dir_path = 'exports/' + datetime.now().strftime('%Y%m%d_%H%M%S')
os.mkdir(new_dir_path)

# Create Technical data
from models.technical import Technical
technical = Technical(sma_periods=[25, 50, 75, 100, 200])
# - SMA
for product in products:
   product.rates = pd.concat([product.rates, technical.generate_close_sma(product)], axis=1)

# Convert format of DATE column from seconds to datetime
for product in products:
   product.rates['time'] = pd.to_datetime(product.rates['time'], unit='s')

# Export CSV
for product in products:
   print('---------------------------')
   print(product.currency_pair_name)

   for sma_period in technical.sma_periods:
      print('---------')
      print(product.rates.iloc[[sma_period], :])

   export_path = new_dir_path + '/' + product.currency_pair_name + '.csv'
   product.rates.to_csv(export_path)

# Instantiate back_test
from models.back_test import BackTest 
back_test = BackTest()

# Back Test
profit_and_loss_dict = {}
for product in products:
   profit_and_loss_dict[product.currency_pair_name] = back_test.search_best_sma_value(technical.sma_periods, product)

# Display results of back test
print('---------------------------')
print('profit_and_loss_dict')
for currency_pair_name, profit_and_loss in profit_and_loss_dict.items():
   print('---------')
   print(currency_pair_name)
   print(profit_and_loss)

# # Visualize
# for product in products:
   # # チャートにティックを表示する
   # plt.plot(product.rates['time'], product.rates['close'], 'r-', label='close')
   
   # # 凡例を表示する
   # plt.legend(loc='upper left')
   
   # # ヘッダを追加する
   # plt.title('AUDUSD close')
   
   # # チャートを表示する
   # plt.show()