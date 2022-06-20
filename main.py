from StockData.QueryAssistanceModule.Query import Query
from StockData.DataDownloadModule.OnlineDataSource import InvestingCom
from StockData.StockDataHolder import StockDataHolder
from DataProcessing.StatisticalDataAnalysis import StatisticalDataAnalysis
from DataPlotting.Histogram import HistogramPlotter
from IndicatorsCalculation.ProbabilisticDataBased import StatisticalTrend
import datetime

days_to_check = 1*360

stock_data = StockDataHolder()
online_db = InvestingCom()
#online_db.get_all_indices_for_country("United States", show=True)

query = Query()
"""wig20 S&P 500 chf/pln Dow 30"""
"""Poland United States"""
query.company = "Dow 30"
query.country = "United States"
query.start_date = datetime.date.today() - datetime.timedelta(days=days_to_check)
query.end_date = datetime.date.today()

stock_data.query = query
stock_data.data_source = online_db
stock_data.init()

stat_data_analysis = StatisticalDataAnalysis(stock_data)
stat_data_analysis.init()
stat_data_analysis.calculate_price_level_strength()

stat_data_analysis.plot().stacked_plot()
stat_data_analysis.plot().price_corridor()

if days_to_check <= 90:
    stat_trend = StatisticalTrend(stock_data=stock_data, data_interval=14)
    stat_trend.calculate_indicator()
    stat_trend.plot()
