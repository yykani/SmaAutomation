import MetaTrader5 as mt5

class TimeFrame:
    M1 = mt5.TIMEFRAME_M1
    M5 = mt5.TIMEFRAME_M5
    M15 = mt5.TIMEFRAME_M15
    M30 = mt5.TIMEFRAME_M30
    H1 = mt5.TIMEFRAME_H1
    H4 = mt5.TIMEFRAME_H4
    D1 = mt5.TIMEFRAME_D1
    W1 = mt5.TIMEFRAME_W1
    MN1 = mt5.TIMEFRAME_MN1

    timeframe_names = {
        M1 : 'M1',
        M5 : 'M5',
        M15 : 'M15',
        M30 : 'M30',
        H1 : 'H1',
        H4 : 'H4',
        D1 : 'D1',
        W1 : 'W1',
        MN1 : 'MN1'
    }
