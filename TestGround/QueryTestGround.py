from StockData.DataDownloadModule.QueryAssistanceModule.Query import Query

import datetime

queryTest = Query()
queryTest.end_date = datetime.date.today() + datetime.timedelta(days=2)
queryTest.company = "chuj"
queryTest.country = "chuj"
print(queryTest.get_dates_array("string"))
