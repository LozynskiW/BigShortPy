from StockData.DataDownloadModule.DataSourceInterface import DataSourceInterface
from StockData.QueryAssistanceModule.ToString import investing_format
import investpy


class InvestingCom(DataSourceInterface):

    def __init__(self):
        self.__query = None

    def set_query(self, query):
        self.__query = query

    def download_data_from_source(self, interval='daily'):
        print("Downloading data for ", interval, "interval")
        try:
            return self.__download_stock_data(interval=interval)
        except RuntimeError:
            print("No stock found, searching for index")
        try:
            return self.__download_index_data(interval=interval)
        except RuntimeError:
            print("No index found, searching for cryptocurrency")
        try:
            return self.__download_cryptocurrency_data(interval=interval)
        except RuntimeError:
            print("No cryptocurrency found, searching for currency pair")
        try:
            return self.__download_currency_data(interval=interval)
        except RuntimeError:
            print("No data found")

        raise AttributeError("No data for given symbol")

    def __download_stock_data(self, interval):
        return investpy.get_stock_historical_data(
            stock=self.__query.company,
            country=self.__query.country,
            from_date=investing_format(self.__query.start_date),
            to_date=investing_format(self.__query.end_date),
            interval=interval)

    def __download_index_data(self, interval):
        return investpy.indices.get_index_historical_data(
            index=self.__query.company,
            country=self.__query.country,
            from_date=investing_format(self.__query.start_date),
            to_date=investing_format(self.__query.end_date),
            interval=interval)

    def __download_cryptocurrency_data(self, interval):
        return investpy.get_crypto_historical_data(
            crypto=self.__query.company,
            from_date=investing_format(self.__query.start_date),
            to_date=investing_format(self.__query.end_date),
            interval=interval)

    def __download_currency_data(self, interval):
        return investpy.get_currency_cross_historical_data(
            currency_cross=self.__query.company,
            from_date=investing_format(self.__query.start_date),
            to_date=investing_format(self.__query.end_date),
            interval=interval)

    @staticmethod
    def get_all_indices_for_country(country, show=False):

        indices = investpy.indices.get_indices(country)

        if show:
            for index in indices['name']:
                print(index)

        return indices