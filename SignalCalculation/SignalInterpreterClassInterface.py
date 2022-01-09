from abc import abstractmethod
import datetime


class PriceLevelBased:
    """
    self.__signal_interpretation = {
            "overpriced": False,
            "underpriced": False,
            "undetermined": True,
            "strength": "strong"
        }
    """
    is_signalInterpreterClass = True
    signal_per_price = []
    _indicators = []

    @abstractmethod
    def set_data(self, data):
        """of type DataProcessing or Indicator"""
        self._indicators = data
        raise NotImplementedError

    @abstractmethod
    def interpret_signals(self):
        raise NotImplementedError

    @abstractmethod
    def get_signal_per_price(self):
        raise NotImplementedError

    @abstractmethod
    def get_signal_for_price(self, price):
        raise NotImplementedError

    @abstractmethod
    def get_signal_for_present_price(self):
        raise NotImplementedError


class DateBased:
    is_signalInterpreterClass = True
    signal_per_date = []

    @abstractmethod
    def set_data(self, *data):
        raise NotImplementedError

    @abstractmethod
    def interpret_signals(self):
        raise NotImplementedError

    @abstractmethod
    def get_signal_per_date(self):
        raise NotImplementedError

    @abstractmethod
    def get_signal_for_date(self, date: datetime.datetime):
        raise NotImplementedError

    @abstractmethod
    def get_signal_for_today(self):
        raise NotImplementedError


class DateAndPriceLevelBased:
    is_signalInterpreterClass = True
    signal_per_date = []
    signal_per_price = []

    @abstractmethod
    def set_data(self, *data):
        raise NotImplementedError

    @abstractmethod
    def interpret_signals(self):
        raise NotImplementedError

    @abstractmethod
    def get_signal_per_date(self):
        raise NotImplementedError

    @abstractmethod
    def get_signal_per_price(self):
        raise NotImplementedError

    @abstractmethod
    def get_signal_for_tomorrow(self):
        raise NotImplementedError