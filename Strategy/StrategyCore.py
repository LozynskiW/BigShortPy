from abc import abstractmethod
from SignalCalculation.SignalInterpreterClassInterface import DateBased, PriceLevelBased, DateAndPriceLevelBased


class StrategyBase:

    is_strategy = True
    min_time_span = 100  # 3 months

    def __init__(self):
        self.__signals = []
        self.__stock_data = None
        self.__analysis_outcome = None
        self.__type_of_strategy = None
        self.__minimal_signals_strength = None

    @abstractmethod
    def set_stock_data(self, stock_data):
        if len(stock_data.raw_data) < self.min_time_span:
            raise ValueError("You need to upload data that contains at least ", self.min_time_span, " days")
        self.__stock_data = stock_data

    @abstractmethod
    def set_signals(self, *signals):

        for signal in signals:
            self.__signals.append(signal)

    @abstractmethod
    def set_strategy_parameters(self, type_of_strategy, minimal_signals_strength):
        """
        Used to predetermine what kind of situations and risk strategy is going to take advantage
        :param minimal_signals_strength:
        Possible minimal_signals_strength types are:
        "strong", "weak", "moderate", "mix"
        Parameter used to determine risk management. Signals may very from weak to strong.
        When parameters is set to "strong" strategy will only play when decision is based on signals that each gave
        strong type of signal. Moderate will allow for single weak signal, and mix will allow for 50% of weak signals
        CAUTION: classification of risk is based only on opinion of it's inventor
        :param type_of_strategy:
        Possible strategy types are:
        "short", "long", "mix"
        For "short" strategy will look for situation where based on signals instrument is overpriced,
        underpriced for "long" and both of situations for "mix"
        :return:
        """
        if type_of_strategy is "short" or type_of_strategy is "long" or type_of_strategy is "mix":

            self.__type_of_strategy = type_of_strategy

        else:
            raise AttributeError("No such type of strategy")

        if minimal_signals_strength is "strong" or \
                minimal_signals_strength is "weak" or \
                minimal_signals_strength is "moderate" or \
                minimal_signals_strength is "moderate":

            self.__minimal_signals_strength = minimal_signals_strength

        else:
            raise AttributeError("No such type of signals strength")

    @abstractmethod
    def develop_strategy_for_stock_data_for_certain_day(self, day):
        """
        Method used to get decision of strategy about trading for certain day. Day must be datetime.date format
        and is used to query StockData for instrument data such as [open_price, close_price, low_price, high_price]
        Decision is based on provided data combined with information from signals or just on provided date when signals
        are based on day indication rather than price indication
        :param day: Day for which decision about trading is to be made
        :return: string indicating trading decision of form: "long", "short" or "wait"
        """
        signals_arr = []

        for signal in self.__signals:

            if type(signal) is DateBased:
                signals_arr.append(signal.get_signal_for_today())

            if type(signal) is PriceLevelBased:
                signals_arr.append(signal.get_signal_for_present_price())

            if type(signal) is DateAndPriceLevelBased:

                signal_day = signal.get_signal_for_today()
                signal_price = signal.get_signal_for_present_price()

                if signal_day is  signal_price:
                    signals_arr.append(signal_price)
                else:
                    signals_arr.append(
                        {
                            "overpriced": False,
                            "underpriced": False,
                            "undetermined": True,
                            "strength": "strong"
                        }
                    )

        for signals in signals_arr:


    @abstractmethod
    def plot(self):
        raise NotImplementedError
