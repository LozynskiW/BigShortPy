from abc import abstractmethod


class IndicatorClassInterface:
    """
    Analysis engine must be set in each class as it is attribute that is never going to change in each implementations
    of any class
    """

    is_indicator = True
    __analysis_engine = None
    __analysis_outcome = None
    __stock_data = None
    __indicator = None

    def set_analysis_engine(self, analysis_engine):
        self.__analysis_engine = analysis_engine

    def get_analysis_engine(self):
        return self.__analysis_engine

    def set_stock_data(self, stock_data):

        if stock_data is None:
            raise AttributeError
        else:
            self.__stock_data = stock_data
            self.__init_analysis_engine(stock_data=self.__stock_data)

    def __init_analysis_engine(self, stock_data):
        self.__analysis_engine.set_stock_data(stock_data=stock_data)
        self.__analysis_engine.init()

    def get_analysis_outcome(self):
        return self.__analysis_engine.get_analysis_outcome()

    def get_indicator(self):
        return self.__indicator

    def set_indicator(self, indicator):
        self.__indicator = indicator

    def get_stock_data(self):
        return self.__stock_data

    def __set_required_analysis_outcome(self, analysis_outcome):
        self.__analysis_outcome = analysis_outcome

    @abstractmethod
    def calculate_indicator(self):
        raise NotImplementedError

    @abstractmethod
    def plot(self):
        raise NotImplementedError
