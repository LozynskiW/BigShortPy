from StockData.DataDownloadModule.QueryAssistanceModule.Query import Query
from StockData.DataDownloadModule.OnlineDataSource import YahooFinance
from StockData.StockDataHolder import StockDataHolder
import datetime

stock_data = StockDataHolder()

query = Query()
"""wig20 ^GSPC"""
query.company = "AAPL"
query.country = "poland"
query.start_date = datetime.date.today() - datetime.timedelta(days=90)
query.end_date = datetime.date.today()

#online_db = InvestingCom()
online_db = YahooFinance()

stock_data.query = query
stock_data.data_source = online_db
stock_data.init()

data = stock_data.get_data(start_date=query.start_date, end_date=query.end_date).dict().daily()

print(data)
