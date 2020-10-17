import datetime
import itertools
from enums.timeframe import TimeFrame

class BackTest:
    interval_days = None
    back_days = None
    test_datetime_from = None
    test_datetime_to = None
    next_datetime_from = None
    next_datetime_to = None
    results = {}

    def __init__(self, interval_days, back_days, test_datetime_from, test_datetime_to):
        self.interval_days = interval_days
        self.back_days = back_days
        self.test_datetime_from = test_datetime_from
        self.test_datetime_to = test_datetime_to
        self.next_datetime_from = test_datetime_from + datetime.timedelta(days=self.back_days)
        self.next_datetime_to = self.next_datetime_from + datetime.timedelta(days=self.back_days)

    def next_period(self):
        self.next_datetime_from += datetime.timedelta(days=self.back_days)
        self.next_datetime_to += datetime.timedelta(days=self.back_days)

    def search_best_sma_value(self, periods, product):
        print('---------------------------')
        print(f'start - search_best_sma_value - from {self.next_datetime_from} to {self.next_datetime_to} - {product.currency_pair_name} - {TimeFrame.timeframe_names[product.timeframe]}')

        profit_and_loss_dict = {}
        
        # 指定されたSMAの期間から3つ選ぶ組み合わせの数だけループ
        for combination in list(itertools.combinations(periods, 3)):
            on_long_trend = False
            on_short_trend = False
            has_position = False
            entry_price = None
            profit_and_loss = 0

            short_term_period = combination[0]
            middle_term_period = combination[1]
            long_term_period = combination[2]
            
            short_term_sma_column_name = 'sma' + str(short_term_period)
            middle_term_sma_column_name = 'sma' + str(middle_term_period)
            long_term_sma_column_name = 'sma' + str(long_term_period)
            
            combination_str = str(short_term_period) + '-' + str(middle_term_period) + '-' + str(long_term_period)
            print(combination_str)

            # ヒストリカルデータを1行ずつ処理
            for index, row in product.rates.iterrows():
                # 長期SMAのデータが存在しない行の場合
                if index < long_term_period:
                    continue
                # Longのトレンドが出ている場合
                if on_long_trend:
                    # ポジションを持っている場合
                    if has_position:
                        # 中期SMA < 長期SMAの場合（中期SMAが長期SMAを上から下に抜けた場合の想定）
                        if row[middle_term_sma_column_name] < row[long_term_sma_column_name]:
                            profit_and_loss += entry_price - row['close']
                            on_long_trend = False
                            has_position = False
                            continue
                    # ポジションを持っていない場合
                    else:
                        # 短期SMA < 中期SMA、且つClose < 長期SMAの場合
                        # （短期SMAが中期SMAを、Closeが長期SMAを上から下に抜けた場合の想定）
                        if row[short_term_sma_column_name] < row[middle_term_sma_column_name] \
                            and \
                            row['close'] < row[long_term_sma_column_name]:
                            has_position = True
                            entry_price = row['close']
                            continue
                # Shortのトレンドが出ている場合
                elif on_short_trend:
                    # ポジションを持っている場合
                    if has_position:
                        # 中期SMA > 長期SMAの場合（中期SMAが長期SMAを下から上に抜けた場合の想定）
                        if row[middle_term_sma_column_name] > row[long_term_sma_column_name]:
                            profit_and_loss += row['close'] - entry_price
                            on_short_trend = False
                            has_position = False
                            continue
                    # ポジションを持っていない場合
                    else:
                        # 短期SMA > 中期SMA、且つClose > 長期SMAの場合
                        # （短期SMAが中期SMAを、Closeが長期SMAを下から上に抜けた場合の想定）
                        if row[short_term_sma_column_name] > row[middle_term_sma_column_name] \
                            and \
                            row['close'] > row[long_term_sma_column_name]:
                            has_position = True
                            entry_price = row['close']
                            continue
                # トレンドが出ていない場合
                else:
                    # 期間が短いSMAが上から順に並んでいる場合、Longのトレンドフラグを立てる
                    if row[short_term_sma_column_name] > \
                        row[middle_term_sma_column_name] > \
                        row[long_term_sma_column_name]:
                        on_long_trend = True
                        continue
                    # 期間が短いSMAが下から順に並んでいる場合、Shortのトレンドフラグを立てる
                    elif row[short_term_sma_column_name] < \
                        row[middle_term_sma_column_name] < \
                        row[long_term_sma_column_name]:
                        on_short_trend = True
                        continue
            
            # pipsに変換して整数に変換
            profit_and_loss = int(profit_and_loss * 10000)
            profit_and_loss_dict[combination_str] = profit_and_loss

            print(f'> {profit_and_loss}')

        results_elem_name = f'from {self.next_datetime_from} to {self.next_datetime_to} - {product.currency_pair_name} - {TimeFrame.timeframe_names[product.timeframe]}'
        self.results[results_elem_name] = profit_and_loss_dict

        return profit_and_loss_dict