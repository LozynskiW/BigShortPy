from abc import ABC

from SignalCalculation.SignalInterpreterClassInterface import PriceLevelBased


class DemandSupplySignal(PriceLevelBased, ABC):

    def __init__(self):
        self.__histogram_data = None
        self.__histogram_data_supply = None
        self.__histogram_data_demand = None
        self.__present_price = 0
        self.__signal_interpretation = {
            "overpriced": False,
            "underpriced": False,
            "undetermined": True,
            "strength": "strong"
        }
        self.__indicator = None

    def set_data(self, data):

        self.__indicator = data
        self.__histogram_data = self.__indicator.get_indicator()['histogram']
        self.__histogram_data_supply = self.__indicator.get_indicator()['histogram_bear']
        self.__histogram_data_demand = self.__indicator.get_indicator()['histogram_bull']
        self.__present_price = self.__indicator.get_indicator()['latest_price']

    def __interpret_signals(self):
        """
        :return:
        signal for present price
        """

        """1, 2"""
        domination_intervals = self.__calculate_domination_intervals()

        if self.__is_stock_price_in_specific_situation(domination_intervals=domination_intervals,
                                                       situation="overpriced"):
            self.__signal_interpretation["overpriced"] = True
            self.__signal_interpretation["undetermined"] = False
            return "short"

        if self.__is_stock_price_in_specific_situation(domination_intervals=domination_intervals,
                                                       situation="underpriced"):
            self.__signal_interpretation["underpriced"] = True
            self.__signal_interpretation["undetermined"] = False
            return "long"

        return "wait"

    def get_signal_per_price(self):
        raise NotImplementedError

    def get_signal_for_price(self, price):
        raise NotImplementedError

    def get_signal_for_present_price(self):

        return self.__interpret_signals()

    def __get_histogram_bin_for_present_price(self):

        if not self.__present_price:
            raise AttributeError("Set data first")

        index = 0

        for hist_bin in self.__histogram_data:

            if hist_bin[0] <= self.__present_price <= hist_bin[1]:
                return index

            index += 1

        raise AttributeError("No histogram bin found to fit present price")

    def __calculate_domination_intervals(self):

        domination_intervals = []
        if self.__histogram_data_supply[0][2] > self.__histogram_data_demand[0][2]:

            domination_intervals.append([self.__histogram_data[0][0], self.__histogram_data[0][0], 'supply'])
        else:
            domination_intervals.append([self.__histogram_data[0][0], self.__histogram_data[0][0], 'demand'])

        for i in range(1, len(self.__histogram_data)):

            examined_interval = domination_intervals[len(domination_intervals) - 1]
            current_price = self.__histogram_data[i][0]

            if self.__histogram_data_supply[i][2] > self.__histogram_data_demand[i][2]:
                if examined_interval[2] == 'supply':
                    domination_intervals[len(domination_intervals) - 1][1] = current_price
                else:
                    domination_intervals.append([current_price, current_price, 'supply'])

            if self.__histogram_data_supply[i][2] < self.__histogram_data_demand[i][2]:
                if examined_interval[2] == 'demand':
                    domination_intervals[len(domination_intervals) - 1][1] = current_price
                else:
                    domination_intervals.append([current_price, current_price, 'demand'])

        return domination_intervals

    def __is_present_price_in_specific_domination_interval(self, domination_intervals, interval_index=0):

        interval = domination_intervals[interval_index]

        if interval[0] < self.__present_price < interval[1]:
            return True

        return False

    @staticmethod
    def __is_specific_interval_of_type(domination_intervals, interval_index=0, domination_type="supply"):

        interval = domination_intervals[interval_index]

        if interval[2] == domination_type:
            return True

        return False

    def __is_stock_price_in_specific_situation(self, domination_intervals, situation="overpriced"):

        if self.__is_specific_interval_of_type(domination_intervals=domination_intervals,
                                               interval_index=len(domination_intervals) - 1,
                                               domination_type="supply"):
            if self.__is_specific_interval_of_type(domination_intervals=domination_intervals,
                                                   interval_index=len(domination_intervals) - 2,
                                                   domination_type="demand"):
                if self.__is_present_price_in_specific_domination_interval(domination_intervals=domination_intervals,
                                                                           interval_index=len(
                                                                               domination_intervals) - 1):
                    if situation == 'overpriced':
                        return True

                if self.__is_present_price_in_specific_domination_interval(domination_intervals=domination_intervals,
                                                                           interval_index=len(
                                                                               domination_intervals) - 2):
                    if situation == 'underpriced':
                        return True

        return False
