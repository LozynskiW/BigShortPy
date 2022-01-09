from abc import ABC

import StockData.StockDataHolder
from IndicatorsCalculation.IndicatorsClassInterface import IndicatorClassInterface
from matplotlib import pyplot as plt


class SupplyOnDemand(IndicatorClassInterface, ABC):

    def __init__(self):
        self.__analysis_outcome = None
        self.__stock_data = None
        self.__supply_on_demand = []

    def set_stock_data(self, stock_data: StockData.StockDataHolder.StockDataHolder):
        self.__stock_data = stock_data

    def set_required_analysis_outcome(self, analysis_outcome):
        self.__analysis_outcome = analysis_outcome

    def calculate_indicator(self):

        data = self.__stock_data.raw_data
        close = data['Close']
        open = data['Open']
        volume = data['Volume']

        supply_on_demand = []

        """pierwsze dane"""
        if close[0] > open[0]:

            supply_on_demand.append(volume[0])
        else:
            supply_on_demand.append(-1*volume[0])

        """reszta"""

        for date in self.__stock_data.convert().to_dates_array(date_format="iso_string"):
            if close[date] > open[date]:
                supply_on_demand.append(volume[date] + supply_on_demand[len(supply_on_demand) - 1])
            else:
                supply_on_demand.append(volume[date] - supply_on_demand[len(supply_on_demand) - 1])

        self.__supply_on_demand = supply_on_demand

    def plot(self):
        plt.plot(self.__supply_on_demand)
