import pandas as pd

class Technical:
    sma_periods = None

    def __init__(self, sma_periods=None):
        if sma_periods != None:
            self.sma_periods = sma_periods

    # SMAデータを生成する
    # product: SMAデータを生成する対象の通貨ペアのインスタンス
    def generate_close_sma(self, product):
        df_sma = pd.DataFrame()

        for sma_period in self.sma_periods:
            df_sma['sma' + str(sma_period)] = product.rates['close'].rolling(sma_period).mean()
        
        return df_sma
