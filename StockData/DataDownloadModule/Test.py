import unittest
import datetime

from StockData.DataDownloadModule.OnlineDataSource import YahooFinance
from StockData.DataDownloadModule.QueryAssistanceModule.Query import Query


class MyTestCase(unittest.TestCase):

    yahoo_finance_data_source = YahooFinance()

    def test_something(self):
        start_date = '10.05.2022'
        end_date = '10.01.2022'
        company = 'AAPL'

        query = Query()
        query.end_date = datetime.datetime.strptime(end_date, '%d.%m.%Y').date()
        query.start_date = datetime.datetime.strptime(start_date, '%d.%m.%Y').date()
        query.company = company

        self.yahoo_finance_data_source.set_query(query=query)

        data_from_source = self.yahoo_finance_data_source.download_data_from_source()

        self.assertEqual(83, len(data_from_source))



if __name__ == '__main__':
    unittest.main()
