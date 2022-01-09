from abc import abstractmethod

from StockData.QueryAssistanceModule.Query import Query


class DataSourceInterface:
    is_data_source = True

    @abstractmethod
    def set_query(self, query: Query):
        raise NotImplementedError

    @abstractmethod
    def download_data_from_source(self, interval='daily'):
        raise NotImplementedError
