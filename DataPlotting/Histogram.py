import copy

from DataPlotting import DataPlottingInterface
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import numpy as np


class StackedHistogramPlotter(DataPlottingInterface.DataPlottingClassInterface):

    def __init__(self):
        self.__analysis_outcome = None
        self.__data = None

    @property
    def analysis_outcome(self):
        return self.__analysis_outcome

    @analysis_outcome.setter
    def analysis_outcome(self, analysis_outcome):

        if len(analysis_outcome) < 0:
            raise ValueError("Length of histogram array is zero, no data to plot")

        if len(analysis_outcome.keys()) < 3:
            raise ValueError("Wrong form of data, impossible to plot")

        if analysis_outcome['histogram'][0][0] == analysis_outcome['histogram'][0][1]:
            raise ValueError("Zero length of histogram bin, impossible to plot")

        self.__analysis_outcome = analysis_outcome

    def set_data(self, data):

        if len(list(data.keys())) < 2:
            raise ValueError("Stacked histogram requires 2 sets of data to plot, try using HistogramPlotter")
        self.__analysis_outcome = data

    def plot_data(self,
                  top="histogram_bull",
                  bottom="histogram_bear",
                  latest_record="on",
                  highlight='on',
                  color_bottom='red',
                  color_top='green'
                  ):

        ox = []
        oy_bottom = []
        oy_top = []

        try:
            histogram_top = self.__analysis_outcome[top]
            histogram_bottom = self.__analysis_outcome[bottom]
            for i in range(0, len(histogram_top)):
                ox.append(histogram_top[i][0])
                oy_bottom.append(histogram_bottom[i][2])
                oy_top.append(histogram_top[i][2])
        except AttributeError:
            print("No such datasets found in provided data")

        plt.figure()
        plt.bar(ox, oy_bottom, align='edge', width=ox[1] - ox[0], color=color_bottom)
        plt.bar(ox, oy_top, align='edge', width=ox[1] - ox[0], color=color_top, bottom=oy_bottom)

        plt.xticks(np.arange(int(np.floor(min(ox)/10))*10, int(np.floor(max(ox)/10))*10+1, 10), rotation=90)

        if latest_record == "on":
            try:
                plt.vlines(self.__analysis_outcome['latest_price'], 0, max(oy_top)+max(oy_bottom), color='black', linewidths=2)
                plt.text(self.__analysis_outcome['latest_price'], max(oy_top)+max(oy_bottom),
                         s=str(self.__analysis_outcome['latest_price']),
                         fontsize=12)
                plt.legend(["latest_record", bottom, top])
            except KeyError:
                plt.legend([bottom, top])

        if highlight == 'on':
            for i in range(0, len(ox) - 1):
                if oy_top[i] > oy_bottom[i]:
                    plt.axvspan(xmin=ox[i], xmax=ox[i + 1], facecolor='green', alpha=0.2)
                elif oy_top[i] < oy_bottom[i]:
                    plt.axvspan(xmin=ox[i], xmax=ox[i + 1], facecolor='red', alpha=0.2)

        plt.title('Prawdopodobieństwo ruchu ceny')
        plt.xlabel('Przedziały cenowe')
        plt.ylabel('Wolumen znormalizowany')
        plt.grid()
        plt.show()


class SubtractedHistogramPlotter(DataPlottingInterface.DataPlottingClassInterface):

    def __init__(self):
        self.__analysis_outcome = None
        self.__data = None

    @property
    def analysis_outcome(self):
        return self.__analysis_outcome

    @analysis_outcome.setter
    def analysis_outcome(self, analysis_outcome):

        if len(analysis_outcome) < 0:
            raise ValueError("Length of histogram array is zero, no data to plot")

        if len(analysis_outcome.keys()) < 3:
            raise ValueError("Wrong form of data, impossible to plot")

        if analysis_outcome['histogram'][0][0] == analysis_outcome['histogram'][0][1]:
            raise ValueError("Zero length of histogram bin, impossible to plot")

        self.__analysis_outcome = analysis_outcome

    def set_data(self, data):
        if len(list(data.keys())) < 2:
            raise ValueError("Subtracted histogram requires 2 sets of data to plot, try using HistogramPlotter")
        self.__analysis_outcome = data

    def plot_data(self,
                  data="histogram_bull",
                  subtract="histogram_bear",
                  latest_record="off",
                  highlight='on',
                  color_when_data_is_lower='red',
                  color_when_data_is_higher='green'
                  ):

        ox = []
        oy_subtract = []
        oy_data = []

        try:
            histogram_data = self.__analysis_outcome[data]
            histogram_subtract = self.__analysis_outcome[subtract]

            oy_subtract = [0 for i in range(0, len(histogram_data))]
            oy_data = copy.deepcopy(oy_subtract)

            for i in range(0, len(histogram_data)):
                ox.append(histogram_data[i][0])
                norm_factor = histogram_data[i][2] + histogram_subtract[i][2] if histogram_data[i][2] + histogram_subtract[i][2] > 0 else 1

                if histogram_data[i][2] - histogram_subtract[i][2] > 0:
                    oy_data[i] = ((histogram_data[i][2] - histogram_subtract[i][2]) / norm_factor) * 100
                else:
                    oy_subtract[i] = ((histogram_subtract[i][2] - histogram_data[i][2]) / norm_factor) * 100

        except AttributeError:
            print("No such datasets found in provided data")

        plt.figure()
        plt.bar(ox, oy_subtract, align='edge', width=ox[1] - ox[0], color=color_when_data_is_lower)
        plt.bar(ox, oy_data, align='edge', width=ox[1] - ox[0], color=color_when_data_is_higher)

        if latest_record == "on":
            try:
                plt.vlines(self.__analysis_outcome['latest_price'], 0, max(oy_data)+max(oy_subtract), color='black', linewidths=2)
                plt.legend(["latest_record", subtract, data])
            except KeyError:
                plt.legend([subtract, data])

        if highlight == 'on':
            for i in range(0, len(ox) - 1):
                if oy_data[i] > oy_subtract[i]:
                    plt.axvspan(xmin=ox[i], xmax=ox[i + 1], facecolor='green', alpha=0.2)
                elif oy_data[i] < oy_subtract[i]:
                    plt.axvspan(xmin=ox[i], xmax=ox[i + 1], facecolor='red', alpha=0.2)

        plt.title('Przewaga popytu lub podaży jako procent przewagi przeważającej siły')
        plt.xlabel('Przedziały cenowe')
        plt.ylabel('% przewagi popytu nad podażą lub podaży nad popytem')
        plt.grid()
        plt.show()


class HistogramPlotter(DataPlottingInterface.DataPlottingClassInterface):

    def __init__(self):
        self.__analysis_outcome = None
        self.__data = None

    @property
    def analysis_outcome(self):
        return self.__analysis_outcome

    @analysis_outcome.setter
    def analysis_outcome(self, analysis_outcome):

        if len(analysis_outcome) < 0:
            raise ValueError("Length of histogram array is zero, no data to plot")

        if analysis_outcome[0][0] == analysis_outcome[0][1]:
            raise ValueError("Zero length of histogram bin, impossible to plot")

        self.__analysis_outcome = analysis_outcome

    def set_data(self, data):
        self.__analysis_outcome = data

    def plot_data(self, data_label='data', plot_title='data in function of normalised volume'):

        histogram_data = self.__analysis_outcome

        ox = []
        oy = []
        for i in range(0, len(histogram_data)):
            ox.append(histogram_data[i][0])
            oy.append(histogram_data[i][2])

        plt.figure()
        plt.bar(ox, oy, align='edge', width=ox[1] - ox[0])

        plt.xlabel('Przedziały cenowe')
        plt.ylabel(data_label)
        plt.title(plot_title)
        plt.grid()
        plt.show()


class AnimatedStackedHistogramPlotter(DataPlottingInterface.DataPlottingClassInterface):

    def __init__(self):
        self.__analysis_outcome = None
        self.__data = None

    @property
    def analysis_outcome(self):
        return self.__analysis_outcome

    @analysis_outcome.setter
    def analysis_outcome(self, analysis_outcome):

        if len(analysis_outcome) < 0:
            raise ValueError("Length of histogram array is zero, no data to plot")

        if len(analysis_outcome.keys()) < 3:
            raise ValueError("Wrong form of data, impossible to plot")

        if analysis_outcome['histogram'][0][0] == analysis_outcome['histogram'][0][1]:
            raise ValueError("Zero length of histogram bin, impossible to plot")

        self.__analysis_outcome = analysis_outcome

    def set_data(self, data):

        if len(list(data.keys())) < 2:
            raise ValueError("Stacked histogram requires 2 sets of data to plot, try using HistogramPlotter")
        self.__analysis_outcome = data

    def prepare_animation(self, bar_container):

        def animate(frame_number):
            # simulate new data coming in
            n, _ = np.histogram(self.__data)

            for count, rect in zip(n, bar_container.patches):
                rect.set_height(count)

            return bar_container.patches

        return animate

    def plot_data(self,
                  top="histogram_bull",
                  bottom="histogram_bear",
                  latest_record="on",
                  highlight='on',
                  color_bottom='red',
                  color_top='green'
                  ):

        ox = []
        oy_bottom = []
        oy_top = []

        try:
            histogram_top = self.__analysis_outcome[top]
            histogram_bottom = self.__analysis_outcome[bottom]
            for i in range(0, len(histogram_top)):
                ox.append(histogram_top[i][0])
                oy_bottom.append(histogram_bottom[i][2])
                oy_top.append(histogram_top[i][2])
        except AttributeError:
            print("No such datasets found in provided data")

        plt.figure()
        plt.bar(ox, oy_bottom, align='edge', width=ox[1] - ox[0], color=color_bottom)
        plt.bar(ox, oy_top, align='edge', width=ox[1] - ox[0], color=color_top, bottom=oy_bottom)

        if latest_record == "on":
            try:
                plt.vlines(self.__analysis_outcome['latest_price'], 0, max(oy_top)+max(oy_bottom), color='black', linewidths=2)
                plt.legend(["latest_record", bottom, top])
            except KeyError:
                plt.legend([bottom, top])

        if highlight == 'on':
            for i in range(0, len(ox) - 1):
                if oy_top[i] > oy_bottom[i]:
                    plt.axvspan(xmin=ox[i], xmax=ox[i + 1], facecolor='green', alpha=0.2)
                elif oy_top[i] < oy_bottom[i]:
                    plt.axvspan(xmin=ox[i], xmax=ox[i + 1], facecolor='red', alpha=0.2)

        plt.title('Prawdopodobieństwo ruchu ceny')
        plt.xlabel('Przedziały cenowe')
        plt.ylabel('Wolumen znormalizowany')
        plt.grid()
        plt.show()