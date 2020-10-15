class sma:
    period = None

    def __init__(self, period):
        if period == None:
            RuntimeError('period is required.')
        self.period = period

    # series: SMAの算出元となる値の配列
    def generateSmaColumnSeries(self, series):

        return series.rolling(self.period).mean()
        