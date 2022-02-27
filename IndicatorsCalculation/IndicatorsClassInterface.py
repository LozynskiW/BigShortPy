from abc import abstractmethod


class IndicatorClassInterface:
    """
    Analysis engine must be set in each class as it is attribute that is never going to change in each implementations
    of any class
    """

    is_indicator = True
    __analysis_engine = None

    @abstractmethod
    def set_stock_data(self, stock_data):

        if self.__analysis_engine is None:
            raise AttributeError
        else:
            self.__init_analysis_engine(stock_data=stock_data)

        self.__set_required_analysis_outcome()

        raise NotImplementedError

    @abstractmethod
    def __set_required_analysis_outcome(self, analysis_outcome):
        raise NotImplementedError

    @abstractmethod
    def __init_analysis_engine(self, stock_data):
        raise NotImplementedError

    @abstractmethod
    def calculate_indicator(self):
        raise NotImplementedError

    @abstractmethod
    def get_indicator(self):
        raise NotImplementedError

    @abstractmethod
    def plot(self):
        raise NotImplementedError
