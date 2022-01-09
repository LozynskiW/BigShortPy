import copy
import datetime
from abc import ABC

from matplotlib import pyplot as plt

from DataPlotting.Corridor import TrendCorridor, HistogramCorridor
from DataProcessing import StatisticalDataAnalysis
from IndicatorsCalculation.IndicatorsClassInterface import IndicatorClassInterface
from StockData.QueryAssistanceModule.Query import Query
from DataProcessing.StatisticalDataAnalysis import StatisticalDataAnalysis


class UnderlyingDataDistribution(IndicatorClassInterface, ABC):
    __stock_data = None
    __analysis_outcome = None
    __indicator = None
    __analysis_engine = None

    def set_stock_data(self, stock_data):
        stock_data.set_main_data('daily')
        self.__init_analysis_engine(stock_data=stock_data)
        self.__set_required_analysis_outcome()
        self.__stock_data = stock_data.raw_data

    def __init_analysis_engine(self, stock_data):
        try:
            super.__analysis_engine = StatisticalDataAnalysis(stock_data)
        except AttributeError:
            print("Error due to stock_data malfunction, stock_data is of proper type")
        except:
            raise AttributeError("Incorrect stock data, or set stock data is not of StockDataHolder type")

    def __set_required_analysis_outcome(self):
        self.__analysis_engine.init()
        self.__analysis_engine.calculate_price_level_strength()
        self.__analysis_outcome = self.__analysis_engine.get_analysis_outcome()

    def calculate_indicator(self):
        self.__indicator = self.__analysis_outcome

    def get_indicator(self):
        return self.__indicator

    def plot(self):
        raise NotImplementedError


class DemandSupplyStrength(IndicatorClassInterface, ABC):
    __stock_data = None
    __analysis_outcome = None
    __indicator = None
    __analysis_engine = None

    """
        self.__analysis_outcome['histogram'] = histogram
        self.__analysis_outcome['histogram_bull'] = histogram_bull
        self.__analysis_outcome['histogram_bear'] = histogram_bear
        self.__analysis_outcome['latest_price'] = self.__close[len(self.__close) - 1]
        
        self.__analysis_outcome['histogram'] = [[poczatek przedziału, koniec przedziału, wolumen znormalizowany],[100, 101, 0.45]...]
        
        self.__stock_data['Close'] = timeseries[['data', wartość], [%d/%m/%Y, 201.58]...]
        self.__stock_data['Open'] = timeseries[['data', wartość], [%d/%m/%Y, 201.58]...]
        self.__stock_data['High'] = timeseries[['data', wartość], [%d/%m/%Y, 201.58]...]
        self.__stock_data['Low'] = timeseries[['data', wartość], [%d/%m/%Y, 201.58]...]
    """

    def set_stock_data(self, stock_data):
        stock_data.set_main_data('daily')
        self.__init_analysis_engine(stock_data=stock_data)
        self.__set_required_analysis_outcome()
        self.__stock_data = stock_data.raw_data

    def __init_analysis_engine(self, stock_data):
        try:
            super.__analysis_engine = StatisticalDataAnalysis(stock_data)
        except AttributeError:
            print("Error due to stock_data malfunction, stock_data is of proper type")
        except:
            raise AttributeError("Incorrect stock data, or set stock data is not of StockDataHolder type")

    def __set_required_analysis_outcome(self):
        self.__analysis_engine.init()
        self.__analysis_engine.calculate_price_level_strength()
        self.__analysis_outcome = self.__analysis_engine.get_analysis_outcome()

    def calculate_indicator(self):

        self.__indicator = copy.deepcopy(self.__stock_data['Close'])

        for i in range(1, len(self.__indicator)):
            close_to_var_factor = (self.__stock_data['Close'][i] - self.__stock_data['Low'][i]) / (
                    self.__stock_data['High'][i] - self.__stock_data['Low'][i])

            index = self.__get_index_for_price(self.__stock_data['Close'][i])

            market_force_strgh = self.__calculate_market_force_strength(index)

            market_strength = self.__analysis_outcome['histogram'][index][2] * market_force_strgh

            self.__indicator[i] = self.__indicator[i - 1] + close_to_var_factor * market_strength

        plt.figure()
        plt.plot(self.__indicator)
        plt.show()

    def get_indicator(self):
        return self.__indicator

    def plot(self):
        raise NotImplementedError

    def __get_index_for_price(self, price):

        for i in range(0, len(self.__analysis_outcome['histogram'])):

            if self.__analysis_outcome['histogram'][i][0] <= price < self.__analysis_outcome['histogram'][i][1]:
                return i

        raise ValueError("Price does not fit any given price level in __analysis_outcome")

    def __calculate_market_force_strength(self, i):

        histogram_data = self.__analysis_outcome['histogram_bull']
        histogram_subtract = self.__analysis_outcome['histogram_bear']

        norm_factor = histogram_data[i][2] + histogram_subtract[i][2] if histogram_data[i][2] + histogram_subtract[i][
            2] > 0 else 1

        return ((histogram_data[i][2] - histogram_subtract[i][2]) / norm_factor) * 100


class StatisticalTrend(IndicatorClassInterface, ABC):
    is_indicator = True

    def __init__(self, stock_data=None, data_interval=None):
        self.__data_processor = StatisticalDataAnalysis(stock_data)
        self.__stock_data = stock_data
        self.__data_interval = data_interval
        self.__analysis_outcomes = []
        self.__trend_plot = {}

    def set_stock_data(self, stock_data):
        stock_data.set_main_data('daily')
        self.__init_analysis_engine(stock_data=stock_data)
        self.__stock_data = stock_data.raw_data

    def set_required_analysis_outcome(self, analysis_outcome):
        self.__analysis_outcomes.append([analysis_outcome])

    def __init_analysis_engine(self, stock_data):
        try:
            super.__analysis_engine = StatisticalDataAnalysis(stock_data)
        except AttributeError:
            print("Error due to stock_data malfunction, stock_data is of proper type")
        except:
            raise AttributeError("Incorrect stock data, or set stock data is not of StockDataHolder type")

    def calculate_indicator(self):

        if self.__stock_data is None:
            raise ValueError("Set stock_data first")

        if self.__data_interval is None:
            raise ValueError("Set data_interval first")

        if not type(self.__data_processor) is StatisticalDataAnalysis:
            raise ValueError("Data_processor must be of StatisticalDataAnalysis kind")

        """
        query.start_date = datetime.date.today() - datetime.timedelta(days=180)
        query.end_date = datetime.date.today()
        """

        query = Query()
        query.company = self.__stock_data.query.company
        query.country = self.__stock_data.query.country
        query.start_date = self.__stock_data.query.start_date
        query.end_date = self.__stock_data.query.start_date + datetime.timedelta(days=self.__data_interval)

        initial_query = copy.deepcopy(self.__stock_data.query)
        self.__stock_data.query = query

        while query.end_date <= initial_query.end_date:
            self.__data_processor.set_stock_data(self.__stock_data)
            self.__data_processor.init()
            self.__data_processor.calculate_price_level_strength()

            self.set_required_analysis_outcome(self.__data_processor.get_analysis_outcome())
            self.__trend_plot[query.end_date] = {
                "histogram": self.__data_processor.get_analysis_outcome()['histogram'],
                "histogram_bull": self.__data_processor.get_analysis_outcome()['histogram_bull'],
                "histogram_bear": self.__data_processor.get_analysis_outcome()['histogram_bear'],
                "expected_value": self.__expected_value(self.__data_processor.get_analysis_outcome()['histogram']),
                "mode": self.__mode(self.__data_processor.get_analysis_outcome()['histogram']),
                "latest_price": self.__data_processor.get_analysis_outcome()['latest_price'],
            }

            query.start_date = self.__stock_data.query.end_date
            query.end_date = self.__stock_data.query.end_date + datetime.timedelta(days=self.__data_interval)
            self.__stock_data.query = query

        self.__stock_data.query = initial_query

    def plot(self):
        plot_engine = HistogramCorridor()
        plot_engine.set_data(self.__trend_plot)
        plot_engine.plot_data()

    def calculate_statistical_parameters(self):

        for key in self.__trend_plot.keys():
            self.__trend_plot[key]["expected_value"] = self.__expected_value(self.__trend_plot[key]['histogram'])
            self.__trend_plot[key]["mode"] = self.__mode(self.__trend_plot[key]['histogram'])

        print(self.__trend_plot.keys())

    @staticmethod
    def __expected_value(array):
        """
        array = [[value1, value2,...,valueN, probability_of_value],[...]...]
        example of array = [[200, 201, 0.324],[201,202, 0.13]...]
        :param array:
        :return:
        """
        expected_value = 0

        for x in array:
            expected_value += x[0] * x[-1]

        return expected_value

    @staticmethod
    def __mode(array):
        mode = 0
        mode_prob = 0

        for x in array:

            if x[2] > mode_prob:
                mode_prob = x[2]
                mode = x[0]

        return mode
