from StockData.QueryAssistanceModule.Query import Query
from StockData.DataDownloadModule.OnlineDataSource import InvestingCom
from StockData.StockDataHolder import StockDataHolder
from DataProcessing.StatisticalDataAnalysis import StatisticalDataAnalysis
from DataPlotting.Histogram import HistogramPlotter
from DataPlotting.Histogram import StackedHistogramPlotter
from DataPlotting.Corridor import PriceCorridor
from IndicatorsCalculation.ProbabilisticDataBased import DemandSupplyStrength
from IndicatorsCalculation.SupplyDemandBased import SupplyOnDemand
from IndicatorsCalculation.ProbabilisticDataBased import StatisticalTrend
import datetime

days_to_check = 180

stock_data = StockDataHolder()

query = Query()
"""wig20 S&P 500 chf/pln"""
"""Poland United States"""
query.company = "wig20"
query.country = "Poland"
query.start_date = datetime.date.today() - datetime.timedelta(days=days_to_check)
query.end_date = datetime.date.today()

online_db = InvestingCom()

stock_data.query = query
stock_data.data_source = online_db
stock_data.init()

stat_data_analysis = StatisticalDataAnalysis(stock_data)
stat_data_analysis.init()
stat_data_analysis.calculate_price_level_strength()

supply_on_demand = SupplyOnDemand()
supply_on_demand.set_stock_data(stock_data=stock_data)
supply_on_demand.calculate_indicator()
supply_on_demand.plot()

stat_data_analysis.plot().stacked_plot()
stat_data_analysis.plot().price_corridor()

stat_trend = StatisticalTrend(stock_data=stock_data, data_interval=14)
stat_trend.calculate_indicator()
stat_trend.plot()