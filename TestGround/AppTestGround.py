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

stock_data = StockDataHolder()

query = Query()
"""wig games wig20"""
query.company = "wig20"
query.country = "poland"
query.start_date = datetime.date.today() - datetime.timedelta(days=360)
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
stat_data_analysis.plot().subtracted_plot()
stat_data_analysis.plot().price_corridor()

"""
test_indicator = DemandSupplyStrength()
test_indicator.set_stock_data(stock_data)
test_indicator.set_required_analysis_outcome(stat_data_analysis)
test_indicator.calculate_indicator()

test_indicator2 = StatisticalTrend(data_processor=stat_data_analysis, stock_data=stock_data, data_interval=30)
test_indicator2.calculate_indicator()
"""
""""""
stat_trend = StatisticalTrend(stock_data=stock_data, data_interval=30)
stat_trend.calculate_indicator()
stat_trend.plot()
