from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd

class product:
    currency_pair_name = ''
    timeframe = None
    datetime_from: datetime|None = None
    datetime_to: datetime|None = None

    def __init__(self, currency_pair_name, timeframe, datetime_from=None, datetime_to=None):
        self.currency_pair_name = currency_pair_name
        self.timeframe = timeframe
        self.datetime_from = datetime_from
        self.datetime_to = datetime_to

    def getRatesRange(self):
        return mt5.copy_rates_range(self.currency_pair_name, self.timeframe, self.datetime_from, self.datetime_to)

    def getRatesDataFrame(self):
        return pd.DataFrame(self.getRatesRange())

    # TODO 単一通貨ペアの情報取得処理を書き、MT5クラスから通貨ペアごとに呼び出す

    # TODO SMAなどのデータ作成処理などの呼び出し処理を書き、mainから呼び出す