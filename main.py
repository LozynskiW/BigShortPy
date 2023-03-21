from StockData.DataDownloadModule.QueryAssistanceModule.Query import Query
from StockData.DataDownloadModule.OnlineDataSource import YahooFinance
from StockData.StockDataHolder import StockDataHolder
from DataProcessing.StatisticalDataAnalysis import StatisticalDataAnalysis
from DataProcessing.InformationEntropyAnalysis import InformationEntropyAnalysis
import datetime

"""wig20 S&P 500 chf/pln Dow 30 ^GSPC"""
"""Poland United States"""

days_to_check = 1*180
years_to_check_arr = [i for i in range(1, 20)]
revs = []
"""
for num_of_years in years_to_check_arr:
    days_to_check = num_of_years*360

    stock_data = StockDataHolder()
    online_db = InvestingCom()
    #online_db.get_all_indices_for_country("United States", show=True)

    query = Query()
    query.company = "S&P 500"
    query.country = "United States"
    query.start_date = datetime.date.today() - datetime.timedelta(days=days_to_check)
    query.end_date = datetime.date.today()

    stock_data.query = query
    stock_data.data_source = online_db
    stock_data.init()

    revenue_stat = RevenueStatics(stock_data=stock_data)
    revenue_stat.init()

    rev = revenue_stat.get_revenue()
    revs.append(rev)

plt.plot(revs)
plt.show()
#revenue_stat.plot()
"""
query = Query()
query.company = "^GSPC"
query.country = "United States"
query.start_date = datetime.date.today() - datetime.timedelta(days=days_to_check)
query.end_date = datetime.date.today()

stock_data = StockDataHolder()
online_db = YahooFinance()
stock_data.query = query
stock_data.data_source = online_db
stock_data.init()

stat_data_analysis = StatisticalDataAnalysis(stock_data)
stat_data_analysis.init()
stat_data_analysis.calculate_price_level_strength()
stat_data_analysis.plot().stacked_plot()

entropy_analysis = InformationEntropyAnalysis(statistical_data_analysis=stat_data_analysis)
entropy_analysis.calculate_information_entropy()
entropy_analysis.get_information_entropy_gradient()
entropy_analysis.get_information_entropy_gradient()
entropy_analysis.plot().bar_plot()
