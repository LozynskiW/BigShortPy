from StockData.QueryAssistanceModule.Query import Query
from StockData.DataDownloadModule.OnlineDataSource import InvestingCom
from StockData.StockDataHolder import StockDataHolder
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

print(stock_data.get_data(start_date=datetime.date(2022, 4, 1), end_date=datetime.date(2022, 4, 10)).dict().daily())