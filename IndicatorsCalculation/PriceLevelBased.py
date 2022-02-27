from IndicatorsCalculation.IndicatorsClassInterface import IndicatorClassInterface
from DataProcessing.StatisticalDataAnalysis import StatisticalDataAnalysis


class PriceLevelProfitability(IndicatorClassInterface):

    is_indicator = True
    __analysis_engine = None

    def __init__(self, analysis_engine, analysis_outcome):
        self.__analysis_engine = analysis_engine
        self.__analysis_outcome = analysis_outcome

    def set_stock_data(self, stock_data):

        if self.__analysis_engine is None:
            raise AttributeError
        else:
            self.__init_analysis_engine(stock_data=stock_data)

        self.__set_required_analysis_outcome(self.__analysis_engine.get_analysis_outcome())

    def __set_required_analysis_outcome(self, analysis_outcome):
        self.__analysis_outcome = analysis_outcome

    def __init_analysis_engine(self, stock_data):
        try:
            super.__analysis_engine = StatisticalDataAnalysis(stock_data)
        except AttributeError:
            print("Error due to stock_data malfunction, stock_data is of proper type")
        except:
            raise AttributeError("Incorrect stock data, or set stock data is not of StockDataHolder type")

    def calculate_indicator(self):
        raise NotImplementedError

    def get_indicator(self):
        raise NotImplementedError

    def plot(self):
        raise NotImplementedError
