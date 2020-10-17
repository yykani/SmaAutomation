# ###########################
# Import common modules
# ###########################
import os
from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5

print(f'### START main.py at {datetime.now()} ###')

# ###########################
# Connect to MetaTrader5
# ###########################
if not mt5.initialize():
   mt5.shutdown()
   raise RuntimeError('initialize() failed')

# ###########################
# Set timezone as utc
# ###########################
import pytz
timezone = pytz.timezone("Etc/UTC")

# ###########################
# Instantiate
# ###########################
# Technical
from models.technical import Technical
technical = Technical(sma_periods=[25, 50, 75, 100, 200])

# BackTest
from models.back_test import BackTest 
back_test = BackTest(
   interval_days = 30,
   back_days = 30,
   test_datetime_from = datetime(2018, 10, 1, tzinfo=timezone),
   test_datetime_to = datetime(2020, 10, 1, tzinfo=timezone)
)

# Calc all loop counts
subtract_period = back_test.test_datetime_to - back_test.next_datetime_from
all_loop_counts = subtract_period.days / back_test.interval_days

for loop_count in range(int(all_loop_counts)):
   # Products
   from models.product import Product
   gbpusd_M5 = Product('GBPUSD', mt5.TIMEFRAME_M5, back_test.next_datetime_from, back_test.next_datetime_to)
   gbpusd_H1 = Product('GBPUSD', mt5.TIMEFRAME_H1, back_test.next_datetime_from, back_test.next_datetime_to)
   gbpusd_H4 = Product('GBPUSD', mt5.TIMEFRAME_H4, back_test.next_datetime_from, back_test.next_datetime_to)

   eurusd_M5 = Product('EURUSD', mt5.TIMEFRAME_M5, back_test.next_datetime_from, back_test.next_datetime_to)
   eurusd_H1 = Product('EURUSD', mt5.TIMEFRAME_H1, back_test.next_datetime_from, back_test.next_datetime_to)
   eurusd_H4 = Product('EURUSD', mt5.TIMEFRAME_H4, back_test.next_datetime_from, back_test.next_datetime_to)

   audusd_M5 = Product('AUDUSD', mt5.TIMEFRAME_M5, back_test.next_datetime_from, back_test.next_datetime_to)
   audusd_H1 = Product('AUDUSD', mt5.TIMEFRAME_H1, back_test.next_datetime_from, back_test.next_datetime_to)
   audusd_H4 = Product('AUDUSD', mt5.TIMEFRAME_H4, back_test.next_datetime_from, back_test.next_datetime_to)

   # ###########################
   # Set DataFrames of rates each currency pairs
   # ###########################
   products = [
      gbpusd_M5,
      gbpusd_H1,
      gbpusd_H4,
      eurusd_M5,
      eurusd_H1,
      eurusd_H4,
      audusd_M5,
      audusd_H1,
      audusd_H4,
   ]
   for product in products:
      product.set_rates_dataframe()

   # ###########################
   # Create a new directory to save csv  
   # ###########################
   new_dir_path = 'exports/' + datetime.now().strftime('%Y%m%d_%H%M%S%f')
   os.mkdir(new_dir_path)

   # ###########################
   # Verification
   # ###########################
   from enums.timeframe import TimeFrame
   profit_and_loss_dict = {}
   for product in products:
      # Create Technical Data
      # - SMA
      product.rates = pd.concat([product.rates, technical.generate_close_sma(product)], axis=1)

      # Convert format of DATE column from seconds to datetime
      product.rates['time'] = pd.to_datetime(product.rates['time'], unit='s')

      # Export CSV
      export_path = new_dir_path + '/' + product.currency_pair_name + '_' + TimeFrame.timeframe_names[product.timeframe] + '.csv'
      product.rates.to_csv(export_path)

      # Back Test
      profit_and_loss_dict[product.currency_pair_name] = back_test.search_best_sma_value(technical.sma_periods, product)

   # ###########################
   # Visualize
   # ###########################
   # from models.visualize import Visualize
   # for product in products:
      # Visualize.visualizeClose(product)

   back_test.next_period()

print('---------------------------')
for key, val in back_test.results.items():
   print(f'{key}: {val}')

# ###########################
# Disconnect from MetaTrader5
# ###########################
mt5.shutdown()

print(f'### FINISH main.py at {datetime.now()} ###')
