from abc import abstractmethod

from StockData.DataDownloadModule.QueryAssistanceModule.Query import Query


class DataSourceInterface:
    is_data_source = True

    @abstractmethod
    def set_query(self, query: Query):
        self.sanitize_query(query)

    @abstractmethod
    def download_data_from_source(self, interval='daily'):
        raise NotImplementedError

    @abstractmethod
    def download_daily_data(self):
        raise NotImplementedError

    @abstractmethod
    def download_weekly_data(self):
        raise NotImplementedError

    @abstractmethod
    def download_monthly_data(self):
        raise NotImplementedError

    @staticmethod
    def sanitize_query(query: Query):

        if query.start_date > query.end_date:

            temp = query.end_date

            query.end_date = query.start_date
            query.start_date = temp