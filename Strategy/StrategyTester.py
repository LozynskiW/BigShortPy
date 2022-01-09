class StrategyTester:

    def __init__(self, interval, instruments_array, data_source, tactics):
        self.__interval = interval
        self.__instruments_array = instruments_array
        self.__data_source = data_source
        self.__tactics = tactics

    def check_tactics(self, start_money=10000):
        raise NotImplementedError
