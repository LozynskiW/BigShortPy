import matplotlib.pyplot as plt

from StockData.QueryAssistanceModule.Query import Query
from StockData.DataDownloadModule.OnlineDataSource import InvestingCom
from StockData.StockDataHolder import StockDataHolder
from DataProcessing.StatisticalDataAnalysis import StatisticalDataAnalysis
from DataProcessing.VolumeDataAnalysis import PurchasePotential
from DataPlotting.Histogram import HistogramPlotter
from DataPlotting.Histogram import StackedHistogramPlotter
from DataPlotting.Corridor import PriceCorridor
from IndicatorsCalculation.ProbabilisticDataBased import DemandSupplyStrength
from IndicatorsCalculation.SupplyDemandBased import SupplyOnDemand
from IndicatorsCalculation.ProbabilisticDataBased import StatisticalTrend
import datetime

stock_data = StockDataHolder()

query = Query()
"""wig20 """
query.company = "wig20"
query.country = "poland"
query.start_date = datetime.date.today() - datetime.timedelta(days=90)
query.end_date = datetime.date.today()

online_db = InvestingCom()

stock_data.query = query
stock_data.data_source = online_db
stock_data.init()

stat_data_analysis = StatisticalDataAnalysis(stock_data)
stat_data_analysis.init()
stat_data_analysis.calculate_price_level_strength()

purchase_potential = PurchasePotential(stock_data)
purchase_potential.calculate_purchase_potential()
purchase_potential.plot()