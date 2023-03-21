from StockData.DataDownloadModule.QueryAssistanceModule.Query import Query
from StockData.DataDownloadModule.OnlineDataSource import InvestingCom
from StockData.StockDataHolder import StockDataHolder
from DataProcessing.StatisticalDataAnalysis import StatisticalDataAnalysis
from SignalCalculation.HistogramBasedSignal import DemandSupplySignal
from TestGround.TestData import TestDataGenerator
import datetime

stock_data = StockDataHolder()

query = Query()
query.company = "wig20"
query.country = "poland"
query.start_date = datetime.date.today() - datetime.timedelta(days=180)
query.end_date = datetime.date.today()

online_db = InvestingCom()

stock_data.query = query
stock_data.data_source = online_db
stock_data.init()

stat_data_analysis = StatisticalDataAnalysis(stock_data)
stat_data_analysis.init()
stat_data_analysis.calculate_price_level_strength()

test_stat_data_analysis = TestDataGenerator()
overpriced_data = test_stat_data_analysis.histogram().overpriced(1000, plot=False)
underpriced_data = test_stat_data_analysis.histogram().underpriced(1000, plot=True)

signal_test = DemandSupplySignal()
signal_test.set_data(stat_data_analysis.get_analysis_outcome())
signal_test.set_data(underpriced_data)
#stat_data_analysis.plot().stacked_plot()
print(signal_test.get_signal_for_present_price())
