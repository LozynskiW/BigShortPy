import copy

import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from matplotlib.gridspec import GridSpec
import seaborn as sns

import StockData.StockDataHolder
from DataPlotting import DataPlottingInterface
from matplotlib import pyplot as plt


class PriceCorridor(DataPlottingInterface.DataPlottingClassInterface):

    def __init__(self):
        self.__analysis_outcome = None
        self.__stock_data = None

    @property
    def analysis_outcome(self):
        return self.__analysis_outcome

    def set_data(self, analysis_outcome):
        if len(analysis_outcome) < 0:
            raise ValueError("Length of histogram array is zero, no data to plot")

        if len(analysis_outcome.keys()) < 4:
            raise ValueError("Wrong form of data, impossible to plot")

        if analysis_outcome['histogram'][0][0] == analysis_outcome['histogram'][0][1]:
            raise ValueError("Zero length of histogram bin, impossible to plot")

        self.__analysis_outcome = analysis_outcome

    @property
    def stock_data(self):
        return self.__stock_data

    @stock_data.setter
    def stock_data(self, stock_data: StockData.StockDataHolder.StockDataHolder):

        if stock_data.raw_data is None:
            raise ValueError("No data in stock data")

        self.__stock_data = stock_data
        self.__stock_data.set_main_data('weekly')

    def plot_data(self, latest_price="off", highlight='on', color_bear='red',
                  color_bull='green'):

        histogram_bull = self.__analysis_outcome['histogram_bull']
        histogram_bear = self.__analysis_outcome['histogram_bear']

        ox_labels = self.__stock_data.convert().to_dates_array()

        close = self.__stock_data.convert().to_np_array(series="Close")
        # open = self.__stock_data.convert().to_np_array(series="Open") no use
        high = self.__stock_data.convert().to_np_array(series="High")
        low = self.__stock_data.convert().to_np_array(series="Low")

        ox = []  # prices
        oy_ticks_range = []
        for i in range(0, len(histogram_bull)):
            ox.append(histogram_bull[i][0])

            if histogram_bull[i][2] is not 0:
                oy_ticks_range.append(histogram_bull[i][1])

        ox_1 = [i for i in range(0, len(high))]

        for i in range(0, len(close)):
            plt.vlines(i, close[i], high[i], color='green', linewidths=2, zorder=1)
            plt.vlines(i, close[i], low[i], color='red', linewidths=2, zorder=1)
        plt.scatter(ox_1, high, marker='_', color='green', linewidths=1, zorder=1)
        plt.scatter(ox_1, low, marker='_', color='red', linewidths=1, zorder=1)
        plt.plot(ox_1, close, color='black')

        for i in range(0, len(histogram_bull) - 1):
            if histogram_bull[i][2] > histogram_bear[i][2]:
                plt.axhspan(ymin=histogram_bull[i][0], ymax=histogram_bull[i + 1][0], facecolor='green', alpha=0.2)
            elif histogram_bull[i][2] < histogram_bear[i][2]:
                plt.axhspan(ymin=histogram_bull[i][0], ymax=histogram_bull[i + 1][0], facecolor='red', alpha=0.2)

        plt.legend(['Cena zamknięcia w danym tygodniu'])
        plt.xticks([i for i in range(0, len(high))], ox_labels, rotation=90)
        plt.yticks(np.arange(int(np.floor(min(oy_ticks_range)/10))*10, int(np.floor(max(oy_ticks_range)/10))*10+1, 20))

        plt.title('Ruch ceny w danych tygodniach')
        plt.xlabel('Tygodnie')
        plt.ylabel('Cena')
        plt.grid()
        plt.show()


class BoxPlotCorridor(DataPlottingInterface.DataPlottingClassInterface):

    def __init__(self):
        self.__analysis_outcome = None
        self.__stock_data = None

    @property
    def analysis_outcome(self):
        return self.__analysis_outcome

    def set_data(self, analysis_outcome):
        if len(analysis_outcome) < 0:
            raise ValueError("Length of histogram array is zero, no data to plot")

        if len(analysis_outcome.keys()) < 4:
            raise ValueError("Wrong form of data, impossible to plot")

        if analysis_outcome['histogram'][0][0] == analysis_outcome['histogram'][0][1]:
            raise ValueError("Zero length of histogram bin, impossible to plot")

        self.__analysis_outcome = analysis_outcome

    @property
    def stock_data(self):
        return self.__stock_data

    @stock_data.setter
    def stock_data(self, stock_data: StockData.StockDataHolder.StockDataHolder):

        if stock_data.raw_data is None:
            raise ValueError("No data in stock data")

        self.__stock_data = stock_data
        self.__stock_data.set_main_data('weekly')

    def plot_data(self, latest_price="off", highlight='on', color_bear='red',
                  color_bull='green'):

        histogram_bull = self.__analysis_outcome['histogram_bull']
        histogram_bear = self.__analysis_outcome['histogram_bear']

        ox_labels = self.__stock_data.convert().to_dates_array()

        close = self.__stock_data.convert().to_np_array(series="Close")
        # open = self.__stock_data.convert().to_np_array(series="Open") no use
        high = self.__stock_data.convert().to_np_array(series="High")
        low = self.__stock_data.convert().to_np_array(series="Low")

        ox = []  # prices
        oy_bear = []
        oy_bull = []
        for i in range(0, len(histogram_bull)):
            ox.append(histogram_bull[i][0])
            oy_bear.append(histogram_bear[i][2])
            oy_bull.append(histogram_bull[i][2])

        ox_1 = [i for i in range(0, len(high))]

        for i in range(0, len(close)):
            plt.vlines(i, close[i], high[i], color='green', linewidths=2, zorder=1)
            plt.vlines(i, close[i], low[i], color='red', linewidths=2, zorder=1)
        plt.scatter(ox_1, high, marker='_', color='green', linewidths=1, zorder=1)
        plt.scatter(ox_1, low, marker='_', color='red', linewidths=1, zorder=1)
        plt.plot(ox_1, close, color='black')

        for i in range(0, len(histogram_bull) - 1):
            if histogram_bull[i][2] > histogram_bear[i][2]:
                plt.axhspan(ymin=histogram_bull[i][0], ymax=histogram_bull[i + 1][0], facecolor='green', alpha=0.2)
            elif histogram_bull[i][2] < histogram_bear[i][2]:
                plt.axhspan(ymin=histogram_bull[i][0], ymax=histogram_bull[i + 1][0], facecolor='red', alpha=0.2)

        plt.legend(['Cena zamknięcia w danym tygodniu'])
        plt.xticks([i for i in range(0, len(high))], ox_labels, rotation=90)

        plt.title('Ruch ceny w danych tygodniach')
        plt.xlabel('Tygodnie')
        plt.ylabel('Cena')
        plt.grid()
        plt.show()


class TrendCorridor(DataPlottingInterface.DataPlottingClassInterface):

    def __init__(self):
        self.__analysis_outcome = None

    @property
    def analysis_outcome(self):
        return self.__analysis_outcome

    def set_data(self, analysis_outcome):
        if len(analysis_outcome) < 0:
            raise ValueError("Length of histogram array is zero, no data to plot")

        if len(analysis_outcome.keys()) < 2:
            raise ValueError("Wrong form of data, impossible to plot")

        self.__analysis_outcome = analysis_outcome

    def plot_data(self, latest_price="off", highlight='on', color_bear='red',
                  color_bull='green'):

        for key in self.__analysis_outcome.keys():

            set = self.__analysis_outcome[key]

            histogram_bull = set['histogram_bull']
            histogram_bear = set['histogram_bear']
            exp_val = set['expected_value']
            mode = set['mode']
            latest_price = set['latest_price']

            oy_bear = []
            oy_bull = []
            ox_bear = []
            ox_bull = []

            for i in range(0, len(histogram_bull), 10):

                if histogram_bull[i][2] < histogram_bear[i][2]:
                    oy_bear.append(histogram_bear[i][1])
                    ox_bear.append(key)
                else:
                    oy_bull.append(histogram_bull[i][1])
                    ox_bull.append(key)

            plt.scatter(key, exp_val, marker="x", color='black', linewidths=5, zorder=3)
            plt.scatter(key, mode, marker="^", color='blue', linewidths=5, zorder=3)
            plt.scatter(key, latest_price, marker=0, color='blue', linewidths=5, zorder=3)
            plt.scatter(ox_bear, oy_bear, marker='.', color='red', linewidths=1, zorder=2)
            plt.scatter(ox_bull, oy_bull, marker='.', color='green', linewidths=1, zorder=2)

        plt.legend(['Trend'])
        # plt.xticks(ox_labels, rotation=90)

        plt.title('Ruch ceny w danych tygodniach')
        plt.xlabel('Tygodnie')
        plt.ylabel('Cena')
        plt.grid()
        plt.show()


class TrendCorridor_OverlappingDensities(DataPlottingInterface.DataPlottingClassInterface):

    def __init__(self):
        self.__analysis_outcome = None

    @property
    def analysis_outcome(self):
        return self.__analysis_outcome

    def set_data(self, analysis_outcome):

        if len(analysis_outcome) < 0:
            raise ValueError("Length of histogram array is zero, no data to plot")

        if len(analysis_outcome.keys()) < 2:
            raise ValueError("Wrong form of data, impossible to plot")

        self.__analysis_outcome = analysis_outcome

    def plot_data(self, latest_price="off", highlight='on', color_bear='red',
                  color_bull='green'):

        fig, axs = plt.subplots(len(self.__analysis_outcome.keys()), sharex=True)

        index = 0

        for dataset_key in self.__analysis_outcome:
            dataset = self.__analysis_outcome[dataset_key]
            start = dataset['from']
            end = dataset['to']

            ox = []
            oy_top = []
            oy_bottom = []

            try:
                histogram_top = dataset['histogram_bull']
                histogram_bottom = dataset['histogram_bear']
                for i in range(0, len(histogram_top)):
                    ox.append(histogram_top[i][0])
                    oy_bottom.append(histogram_bottom[i][2])
                    oy_top.append(histogram_top[i][2] + histogram_bottom[i][2])
            except AttributeError:
                print("No such datasets found in provided data")

            axs[index].bar(ox, oy_bottom, align='edge', width=ox[1] - ox[0], color=color_bear, alpha=0.5)
            axs[index].bar(ox, oy_top, align='edge', width=ox[1] - ox[0], color=color_bull, bottom=oy_bottom, alpha=0.5)

            open_price = dataset['open_price']
            close_price = dataset['close_price']
            expected_val = dataset['expected_value']
            """Dane przesunięte o tydzień do przodu xD- TO DO"""
            print("from:", str(start), "to:", str(end), "open:", open_price, "close:", close_price)

            axs[index].vlines(open_price, 0, np.max(oy_bottom) + np.max(oy_top), color='blue', linewidths=2, zorder=1)
            axs[index].text(open_price, 0, 'open', rotation=90)

            axs[index].vlines(close_price, 0, np.max(oy_bottom) + np.max(oy_top), color='blue', linewidths=2, zorder=1)
            axs[index].text(close_price, 0, 'close', rotation=90)

            axs[index].vlines(expected_val, 0, np.max(oy_bottom) + np.max(oy_top), color='black', linewidths=2,
                              zorder=1)

            axs[index].set_title(str(start) + " - " + str(end))

            axs[index].spines["right"].set_visible(False)
            axs[index].spines["top"].set_visible(False)

            if index == len(self.__analysis_outcome) - 1:
                axs[index].set_xlabel("Price bin")

            index += 1

        fig.tight_layout()
        fig.patch.set_visible(False)
        plt.show()

    def __get_min_and_max_bin_values(self):

        min_val = 100000000
        max_val = 0
        hist_bins = []

        for dataset_key in self.__analysis_outcome.keys():
            dataset = self.__analysis_outcome[dataset_key]
            hist_bins = list(map(lambda d: d[0], dataset['histogram']))

            if min(hist_bins) < min_val:
                min_val = min(hist_bins)

            if max(hist_bins) > max_val:
                max_val = max(hist_bins)

        precision = hist_bins[1] - hist_bins[0]

        return int(min_val), int(max_val), int(precision)

    def __determine_boundaries_for_dataset(self, key, min_val, max_val, prec):
        """
        function to determine how many zeros needs to be added for each dataset so that all datasets have equal length
        :param key:
        :param min_val:
        :param max_val:
        :param prec:
        :return:
        """
        dataset = None

        try:
            dataset = self.__analysis_outcome[key]

        except KeyError:
            raise KeyError("No such key in given analysis_outcomes")

        num_of_zeros_to_add_before_start = int((dataset[0][0] - min_val) / prec)
        num_of_zeros_to_add_to_end = int((max_val - dataset[len(dataset) - 1][0]) / prec)

        return num_of_zeros_to_add_before_start, num_of_zeros_to_add_to_end

    def __get_all_data_to_one_x(self):

        min_val, max_val, prec = self.__get_min_and_max_bin_values()

        for dataset_key in self.__analysis_outcome.keys():

            num_of_zeros_to_add_before_start, num_of_zeros_to_add_to_end = self.__determine_boundaries_for_dataset(
                key=dataset_key,
                min_val=min_val,
                max_val=max_val,
                prec=prec
            )

            for key in ['histogram', 'histogram_bull', "histogram_bear"]:
                for data in self.__analysis_outcome[key]:
                    for i in range(0, num_of_zeros_to_add_before_start):
                        self.__analysis_outcome[dataset_key][key].insert(0, [0, 0, 0])
                    for i in range(0, num_of_zeros_to_add_to_end):
                        self.__analysis_outcome[dataset_key][key].insert(len(self.__analysis_outcome[dataset_key][key]),
                                                                         [0, 0, 0])


class HistogramCorridor(DataPlottingInterface.DataPlottingClassInterface):
    """Przekombinowane, funkcjca ma służyć do pokazywania histogramów w danym okresie, na razie to wystarczy, obecnie
    nie do końca wiadomo co jest wyświetlane i powstają problemy z normalizacją wyników"""

    def __init__(self):
        self.__analysis_outcome = None

    @property
    def analysis_outcome(self):
        return self.__analysis_outcome

    def set_data(self, analysis_outcome):
        if len(analysis_outcome) < 0:
            raise ValueError("Length of histogram array is zero, no data to plot")

        if len(analysis_outcome.keys()) < 2:
            raise ValueError("Wrong form of data, impossible to plot")

        self.__analysis_outcome = analysis_outcome

    def plot_data(self, latest_price="off", highlight='on', color_bear='red',
                  color_bull='green'):

        colormaps = [self.cmap()]

        data = []

        min_val, max_val, prec = self.__get_min_and_max_bin_values()

        for dataset_key in self.__analysis_outcome:

            dataset = self.__analysis_outcome[dataset_key]
            data_to_plot = []
            hist_bull = dataset['histogram_bull']
            hist_bear = dataset['histogram_bear']
            i = 0

            for val in range(0, min_val, prec):
                data_to_plot.append(0)

            for val in range(min_val, max_val, prec):

                """
                if histogram_data[i][2] - histogram_subtract[i][2] > 0:
                    oy_data[i] = ((histogram_data[i][2] - histogram_subtract[i][2]) / norm_factor) * 100
                else:
                    oy_subtract[i] = ((histogram_subtract[i][2] - histogram_data[i][2]) / norm_factor) * 100
                """

                if hist_bull[0][0] <= val < hist_bull[len(hist_bull) - 1][0] and hist_bear[i][2] + hist_bull[i][2] != 0:

                    norm_factor = hist_bear[i][2] + hist_bull[i][2]
                    vol_impact = (hist_bull[i][2] + hist_bear[i][2]) * 100

                    data_to_plot.append(int(
                        vol_impact * ((hist_bull[i][2] - hist_bear[i][2]) / norm_factor) * 100
                    ))

                    i += 1

                else:
                    data_to_plot.append(0)
            data.append(data_to_plot)
        """
        x_ticks_len = len(data)
        data = self.transpose_to_plot(data)
        n = len(colormaps)
        fig, axs = plt.subplots(1, n, figsize=(n * 2 + 2, 3),
                                constrained_layout=True, squeeze=False)
        for [ax, cmap] in zip(axs.flat, colormaps):
            psm = ax.pcolormesh(data, cmap=cmap, rasterized=True)
            fig.colorbar(psm, ax=ax)

        plt.ylim(min_val - 0.05*min_val, max_val+0.05*max_val)
        plt.xticks([i for i in range(0, x_ticks_len)], self.__analysis_outcome.keys(), rotation=90)
        plt.grid()
        """
        plt.figure()
        for dataset_key in self.__analysis_outcome:
            dataset = self.__analysis_outcome[dataset_key]

            ox = []
            oy_bottom = []
            oy_top = []

            try:
                histogram_top = dataset['histogram_bull']
                histogram_bottom = dataset['histogram_bear']
                for i in range(0, len(histogram_top)):
                    ox.append(histogram_top[i][0])
                    oy_bottom.append(histogram_bottom[i][2])
                    oy_top.append(histogram_top[i][2] + histogram_bottom[i][2])
            except AttributeError:
                print("No such datasets found in provided data")

            plt.stem(ox, oy_bottom, color="red")
            plt.stem(ox, oy_top, color="green")
            plt.fill_between(ox, oy_bottom, step="pre", alpha=0.4, color="red")
            plt.fill_between(ox, y1=oy_bottom, y2=oy_top, step="pre", alpha=0.4, color="green")

        plt.grid()
        plt.show()

    def __get_min_and_max_bin_values(self):

        min_val = 100000000
        max_val = 0
        hist_bins = []

        for dataset_key in self.__analysis_outcome:
            dataset = self.__analysis_outcome[dataset_key]
            hist_bins = list(map(lambda d: d[0], dataset['histogram']))

            if min(hist_bins) < min_val:
                min_val = min(hist_bins)

            if max(hist_bins) > max_val:
                max_val = max(hist_bins)

        precision = hist_bins[1] - hist_bins[0]

        return int(min_val), int(max_val), int(precision)

    @staticmethod
    def transpose_to_plot(matrix):

        t_matrix = []

        for i in range(0, len(matrix[0])):
            t_matrix.append([])

            for e in matrix:
                t_matrix[len(t_matrix) - 1].append(e[i])

        return t_matrix

    @staticmethod
    def cmap():

        return ListedColormap(['darkred', 'red', 'indianred', 'salmon', 'mistyrose',
                               'white',
                               'lightyellow', 'palegoldenrod', 'lightgreen', 'yellowgreen', 'olivedrab'])

    @staticmethod
    def transfer_matrix_to_image(matrix, cmap):
        """cmap = [min value, max value, color]"""

        if not cmap:
            raise AttributeError("No cmap to convert values of matrix to colors")

        image = copy.deepcopy(matrix)

        for i, j in np.shape(matrix):

            for c in cmap:
                if c[0] < matrix[i][j] < c[1]:
                    image[i][j] = c[2]
