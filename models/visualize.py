import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

class Visualize:

    def visualizeClose(self, product):
        # チャートにティックを表示する
        plt.plot(product.rates['time'], product.rates['close'], 'r-', label='close')
        
        # 凡例を表示する
        plt.legend(loc='upper left')
        
        # ヘッダを追加する
        plt.title(f'{product.currency_pair_name} - {product.timeframe} - close')
        
        # チャートを表示する
        plt.show()