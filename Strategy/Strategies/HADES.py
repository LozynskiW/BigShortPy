class Hades:
    """
    Histogram
    Approved
    Demand
    End?
    Supply
    """
    min_time_span = 100  # 3 months

    def __init__(self):
        self.__signal = None
        self.__stock_data = None
        self.__analysis_outcome = None
        self.__type_of_strategy = None
        self.__minimal_signals_strength = None

    def set_strategy_parameters(self, type_of_strategy, minimal_signals_strength):

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

    def set_stock_data(self, stock_data):
        if len(stock_data.raw_data) < self.min_time_span:
            raise ValueError("You need to upload data that contains at least ", self.min_time_span, " days")
        self.__stock_data = stock_data

    def devise_strategy(self):
        raise NotImplementedError

    def plot(self):
        raise NotImplementedError
