from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
from typing import Union

class Product:
    currency_pair_name = ''
    timeframe = None
    datetime_from: Union[datetime, None] = None
    datetime_to: Union[datetime, None] = None
    rates: pd.DataFrame = None

    def __init__(self, currency_pair_name, timeframe, datetime_from=None, datetime_to=None):
        self.currency_pair_name = currency_pair_name
        self.timeframe = timeframe
        self.datetime_from = datetime_from
        self.datetime_to = datetime_to

    def get_rates_range(self):
        rates = mt5.copy_rates_range(self.currency_pair_name, self.timeframe, self.datetime_from, self.datetime_to)
        if rates != None:
            return rates
        else:
            raise RuntimeError('copy_rates_range() failed. error code =', mt5.last_error())

    def set_rates_dataframe(self):
        self.rates = pd.DataFrame(self.get_rates_range())

    # TODO 単一通貨ペアの情報取得処理を書き、MT5クラスから通貨ペアごとに呼び出す

    # TODO SMAなどのデータ作成処理などの呼び出し処理を書き、mainから呼び出す