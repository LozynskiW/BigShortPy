import copy
import datetime
from abc import ABC

import scipy.stats
import scipy.stats as stat

import numpy as np
from matplotlib import pyplot as plt

from DataPlotting.Corridor import TrendCorridor, HistogramCorridor, TrendCorridor_OverlappingDensities, BoxPlotCorridor, \
    PriceCorridor, BasicCorridor
from DataProcessing import StatisticalDataAnalysis

from DataPlotting.Histogram import HistogramPlotter
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
        self.set_data_interval(data_interval=data_interval)
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

    def set_data_interval(self, data_interval):

        if not data_interval in [7, 14, 30]:
            raise ValueError("Possible intervals are: 7d, 14d, 30d")

        self.__data_interval = data_interval

    def calculate_indicator(self):

        if self.__stock_data is None:
            raise ValueError("Set stock_data first")

        if self.__data_interval is None:
            raise ValueError("Set data_interval first")

        if not type(self.__data_processor) is StatisticalDataAnalysis:
            raise ValueError("Data_processor must be of StatisticalDataAnalysis kind")

        time_intervals = self.calculate_time_intervals()
        time_intervals.reverse()

        query = Query()
        query.company = self.__stock_data.query.company
        query.country = self.__stock_data.query.country
        query.start_date = time_intervals[0][1]
        query.end_date = time_intervals[0][0]

        initial_query = copy.deepcopy(self.__stock_data.query)
        self.__stock_data.query = query
        self.__trend_plot = {}

        for time_interval in time_intervals:
            query.start_date = time_interval[1]
            query.end_date = time_interval[0]
            self.__stock_data.query = query
            self.__stock_data.init()

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
                "from": time_interval[1],
                "to": time_interval[0],
                "open_price": self.__stock_data.raw_data['Open'][0],
                "close_price": self.__stock_data.raw_data['Close'][-1]
            }

        self.__stock_data.query = initial_query

    def plot(self):
        plot_engine = TrendCorridor_OverlappingDensities()
        plot_engine.set_data(self.__trend_plot)
        plot_engine.plot_data(latest_price='on')

    def calculate_statistical_parameters(self):

        for key in self.__trend_plot.keys():
            self.__trend_plot[key]["expected_value"] = self.__expected_value(self.__trend_plot[key]['histogram'])
            self.__trend_plot[key]["mode"] = self.__mode(self.__trend_plot[key]['histogram'])

    def calculate_time_intervals(self):
        """
        Method to calculate and return list of time intervals to calculate data
        return in form of [[from, to],[from, to]...]
        :return:
        """
        time_intervals = []

        weeks_intervals = self.__calculate_weeks_intervals()

        weeks_intervals[len(weeks_intervals) - 1][1] = self.__stock_data.query.end_date
        weeks_intervals.reverse()

        num_of_weeks_intervals_in_time_interval = int(self.__data_interval / 7)

        for week_num in range(num_of_weeks_intervals_in_time_interval, len(weeks_intervals) + 1,
                              num_of_weeks_intervals_in_time_interval):
            time_interval = [weeks_intervals[week_num - num_of_weeks_intervals_in_time_interval][1],
                             weeks_intervals[week_num - 1][0]]

            time_intervals.append(time_interval)

        return time_intervals

    def __calculate_weeks_intervals(self):
        """
        Method to calculate and return list of raw time intervals
        :return:
        """

        weeks_intervals = []

        day_num = self.__stock_data.query.start_date.isoweekday()

        week_start = self.__stock_data.query.start_date - datetime.timedelta(days=day_num - 1)
        week_end = self.__stock_data.query.start_date + datetime.timedelta(days=5 - day_num)

        week = [week_start, week_end]
        weeks_intervals.append(week)

        while self.__stock_data.query.end_date > week_start + datetime.timedelta(days=7):
            week_start = week_start + datetime.timedelta(days=7)
            week_end = week_end + datetime.timedelta(days=7)

            week = [week_start, week_end]
            weeks_intervals.append(week)

        return weeks_intervals

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


class RegressionToMean(IndicatorClassInterface, ABC):
    is_indicator = True

    def __init__(self):
        super().set_analysis_engine(StatisticalDataAnalysis())
        self.__analysis_outcome = []
        self.__indicator = None
        self.__plot_engine = BoxPlotCorridor()

    def calculate_indicator(self, type='moving_average', data_interval=7, window_size=10, sample_position='middle'):

        if type not in ['moving_average', 'full_weeks']:
            raise ValueError("Not supported types")

        if super().get_stock_data() is None:
            raise ValueError("Set stock_data first")

        if data_interval == 'full_weeks' and (data_interval not in [7, 14, 30]):
            raise ValueError("For 'full_weeks' type data interval must be 7 or 14 or 30")

        if type == 'moving_average':
            return self.__calculate_for_moving_average(dates_array=super().get_stock_data().get_dates_arrays_dict()['daily'],
                                                       stock_data=super().get_stock_data(),
                                                       window_size=window_size,
                                                       sample_position=sample_position)

        if type == 'full_weeks':
            bull_exp_vals = []
            bear_exp_vals = []
            exp_vals = []

            data_in_intervals = super().get_stock_data().convert().divided_into_intervals(interval=7)

            dates_array = super().get_stock_data().get_dates_arrays_dict()['daily']

            for data_for_interval in data_in_intervals:
                close = list(map(lambda x: x[0]['Close'], data_for_interval[0]['data']))
                high = list(map(lambda x: x[0]['High'], data_for_interval[0]['data']))
                low = list(map(lambda x: x[0]['Low'], data_for_interval[0]['data']))
                open = list(map(lambda x: x[0]['Open'], data_for_interval[0]['data']))
                volume = list(map(lambda x: x[0]['Volume'], data_for_interval[0]['data']))

                super().get_analysis_engine().set_data_manually(close=close, high=high, low=low, open=open, volume=volume)

                histogram_bear, histogram_bull, histogram = super().get_analysis_engine().calculate_price_level_strength()

                bull_weights = list(map(lambda x: x[2], histogram_bull))
                bear_weights = list(map(lambda x: x[2], histogram_bear))
                weights = list(map(lambda x: x[2], histogram))

                price_values = list(map(lambda x: x[1], histogram))

                bull_exp_vals.append(stat.gmean(a=price_values, weights=bull_weights))
                bear_exp_vals.append(stat.gmean(a=price_values, weights=bear_weights))
                exp_vals.append(stat.gmean(a=price_values, weights=weights))

    def __calculate_for_weeks(self):

        bull_exp_vals = []
        bear_exp_vals = []
        exp_vals = []

        data_in_intervals = super().get_stock_data().convert().divided_into_intervals(interval=7)

        for data_for_interval in data_in_intervals:
            close = list(map(lambda x: x[0]['Close'], data_for_interval[0]['data']))
            high = list(map(lambda x: x[0]['High'], data_for_interval[0]['data']))
            low = list(map(lambda x: x[0]['Low'], data_for_interval[0]['data']))
            open = list(map(lambda x: x[0]['Open'], data_for_interval[0]['data']))
            volume = list(map(lambda x: x[0]['Volume'], data_for_interval[0]['data']))

            super().get_analysis_engine().set_data_manually(close=close, high=high, low=low, open=open, volume=volume)

            histogram_bear, histogram_bull, histogram = super().get_analysis_engine().calculate_price_level_strength()

            bull_exp_vals.append(self.__expected_val(histogram_bull))
            bear_exp_vals.append(self.__expected_val(histogram_bear))
            exp_vals.append(self.__expected_val(histogram))

    def __calculate_for_moving_average(self, dates_array, stock_data, window_size=10, sample_position='middle'):

        bull_exp_vals = {}
        bear_exp_vals = {}
        exp_vals = {}

        for date_to_calculate_ma in dates_array:

            start_date = date_to_calculate_ma

            try:
                dict_data = stock_data.get_data(start_date=start_date-datetime.timedelta(days=window_size), end_date=start_date).dict().daily()

                close = self.__get_data_from_dict(dict_data, 'Close')
                high = self.__get_data_from_dict(dict_data, 'High')
                low = self.__get_data_from_dict(dict_data, 'Low')
                open = self.__get_data_from_dict(dict_data, 'Open')
                volume = self.__get_data_from_dict(dict_data, 'Volume')

                super().get_analysis_engine().set_data_manually(close=close, high=high, low=low, open=open,
                                                                volume=volume)

                histogram_bear, histogram_bull, histogram = super().get_analysis_engine().calculate_price_level_strength()

                bull_weights = list(map(lambda x: x[2], histogram_bull))
                bear_weights = list(map(lambda x: x[2], histogram_bear))
                weights = list(map(lambda x: x[2], histogram))
                price_values = list(map(lambda x: x[1], histogram))

                exp_vals[date_to_calculate_ma] = np.average(a=price_values, weights=weights)
                bull_exp_vals[date_to_calculate_ma] = np.average(a=price_values, weights=bull_weights)
                bear_exp_vals[date_to_calculate_ma] = np.average(a=price_values, weights=bear_weights)

            except ValueError:
                continue

        multiply_factor = 2

        for key in exp_vals.keys():

            if bull_exp_vals[key] > exp_vals[key] > bear_exp_vals[key] or (bull_exp_vals[key] > bear_exp_vals[key]):
                bull_exp_vals[key] += multiply_factor * scipy.stats.entropy(bull_weights, base=2)
                bear_exp_vals[key] -= multiply_factor * scipy.stats.entropy(bear_weights, base=2)
            elif (bear_exp_vals[key] > exp_vals[key] > bull_exp_vals[key]) or (bear_exp_vals[key] > bull_exp_vals[key]):
                bull_exp_vals[key] -= multiply_factor * scipy.stats.entropy(bull_weights, base=2)
                bear_exp_vals[key] += multiply_factor * scipy.stats.entropy(bear_weights, base=2)


        self.__indicator = {
            "bull_exp_vals": bull_exp_vals,
            "bear_exp_vals": bear_exp_vals,
            "exp_vals": exp_vals
        }
        return bull_exp_vals, bear_exp_vals, exp_vals

    @staticmethod
    def __get_data_from_dict(data_dict, key):

        output_array = []

        for k in data_dict.keys():
            output_array.append(data_dict[k][0][key])

        return output_array

    @staticmethod
    def __check_dates(sample_position, start_date, window_size, date):

        if sample_position not in ['middle', 'left', 'right']:
            raise ValueError("No such window_position supported")

        if sample_position == 'middle':

            if start_date - datetime.timedelta(days=int(window_size / 2)) <= date < start_date + datetime.timedelta(
                    days=int(window_size / 2)):
                return True
            else:
                return False

        if sample_position == 'right':

            if start_date - datetime.timedelta(days=window_size) < date >= start_date:
                return True
            else:
                return False

        if sample_position == 'left':

            if start_date <= date > start_date + datetime.timedelta(days=window_size):
                return True
            else:
                return False

        return False

    def plot(self):
        plot_engine = BasicCorridor()
        plot_engine.set_data(self.__indicator)
        plot_engine.stock_data = super().get_stock_data()
        plot_engine.plot_data()

    @staticmethod
    def __expected_val(histogram):

        exp_val = 0
        p = 0

        for i in histogram:
            exp_val += i[1] * i[2]
            p += i[2]

        return exp_val

    @staticmethod
    def __std(histogram, mean):

        std = 0
        for i in histogram:

            std += (i[1] - mean)**2

        std = std/(len(histogram)-1)

        return np.sqrt(std)


class InformationEntropyAnalysis(IndicatorClassInterface, ABC):

    def __init__(self, stock_data):
        super().set_analysis_engine(StatisticalDataAnalysis())
        super().set_stock_data(stock_data)

    def calculate_indicator(self, normalisation=False):

        analysis_outcome = super().get_analysis_outcome()
        histogram_data = copy.deepcopy(analysis_outcome['histogram'])

        for i in range(0, len(histogram_data)):
            if histogram_data[i][2] > 0:
                p = histogram_data[i][2]
                histogram_data[i][2] = -1 * np.log2(p) * p

        if normalisation:
            mean = np.mean(list(map(lambda x: x[2], histogram_data)))

            if normalisation == 'std':
                std = np.std(list(map(lambda x: x[2], histogram_data)))

                for i in range(0, len(histogram_data)):
                    histogram_data[i][2] = (histogram_data[i][2] - mean) / std
            if normalisation == 'mean':
                for i in range(0, len(histogram_data)):
                    histogram_data[i][2] = histogram_data[i][2] / mean

        super().set_indicator(histogram_data)

    def get_information_entropy_gradient(self):

        histogram_entropy_gradient_data = copy.deepcopy(super().get_indicator())

        for i in range(1, len(histogram_entropy_gradient_data)):
            histogram_entropy_gradient_data[i][2] = histogram_entropy_gradient_data[i][2] - \
                                                    histogram_entropy_gradient_data[i - 1][2]

        return histogram_entropy_gradient_data

    def plot(self):
        return self.__DataPlotter(stock_data=super().get_stock_data(), entropy_data_analysis=super().get_indicator())

    class __DataPlotter:

        __histogram_plotter = HistogramPlotter()
        __price_corridor = PriceCorridor()

        def __init__(self, stock_data, entropy_data_analysis):
            self.__stock_data = stock_data
            self.__entropy_data_analysis = entropy_data_analysis

        def price_corridor(self):
            self.__price_corridor.set_data(self.__entropy_data_analysis)

            self.__price_corridor.stock_data = self.__stock_data

            self.__price_corridor.plot_data(division_type='value', division_value=1)
