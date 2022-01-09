import copy
import datetime

import pandas.core.frame

import StockData.QueryAssistanceModule.Query


class StockDataHolder:
    __raw_data = None
    __data_source = None
    __data = {}
    __query = None

    @property
    def data_source(self):
        return self.__data_source

    @data_source.setter
    def data_source(self, data_source):

        if not data_source.is_data_source:
            raise ValueError("Query must inherit after DataDownloadModule.DataSourceInterface.DataSourceInterface")
        self.__data_source = data_source

    @property
    def query(self):
        return self.__query

    @query.setter
    def query(self, query):

        if type(query) is not StockData.QueryAssistanceModule.Query.Query:
            raise ValueError("Query must be a query object")
        self.__query = query

    @property
    def raw_data(self):
        return self.__raw_data

    @raw_data.setter
    def raw_data(self, raw_data):
        self.__raw_data = raw_data

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        if type(data) is not type(self.__data):
            raise ValueError("Stock data must be dictionary")
        self.__data = data

    def init(self):
        if self.__query is None or self.__data_source is None:
            raise AttributeError("First make sure query and data source is set")
        self.set_query_for_datasource()

        self.__data['daily'] = self.__save_data().daily()
        self.__data['weekly'] = self.__save_data().weekly()
        self.__data['monthly'] = self.__save_data().monthly()

        self.raw_data = self.__data['daily']

    def set_query_for_datasource(self):
        self.__data_source.set_query(self.__query)

    def set_main_data(self, interval='daily'):

        if interval == 'daily':
            self.__raw_data = self.__data['daily']
        if interval == 'weekly':
            self.__raw_data = self.__data['weekly']
        if interval == 'monthly':
            self.__raw_data = self.__data['monthly']

    def convert(self):
        return self.__Convert(self, self.__query)

    def get_data(self):
        return self.__DataGiveaway(self)

    def __save_data(self):
        return self.__DataDownload(self.__data_source, self.__query)

    class __DataGiveaway:

        def __init__(self, data):
            self.__data_source = data

        def daily(self):
            return self.__data_source['daily']

        def weekly(self):
            return self.__data_source['weekly']

        def monthly(self):
            return self.__data_source['monthly']

    class __DataDownload:

        def __init__(self, data_source, query):
            self.__data_source = data_source
            self.__query = query

        def daily(self):
            return self.__data_source.download_data_from_source(interval='daily')

        def weekly(self):
            return self.__data_source.download_data_from_source(interval='weekly')

        def monthly(self):
            return self.__data_source.download_data_from_source(interval='monthly')

    class __Convert:

        def __init__(self, stock_data, query):
            self.__stock_data = stock_data
            self.__query = query

        @staticmethod
        def to_dict(raw_data):
            if type(raw_data) is pandas.core.frame.DataFrame:
                return raw_data.to_dict('series')
            raise ValueError("Data must be panda DataFrame")

        def to_np_array(self, series):

            out = []

            for d in self.__stock_data.query.get_dates_array(date_format='iso_string'):
                try:
                    out.append(self.__stock_data.raw_data[series][d])
                except KeyError:
                    continue

            return out

        def to_dates_array(self, date_format="datetime"):

            out = []

            for d in self.__stock_data.query.get_dates_array(date_format='iso_string'):

                try:
                    temp = self.__stock_data.raw_data['Close'][d]
                    out.append(datetime.datetime.strptime(d, "%Y-%m-%d").date())
                except KeyError:
                    continue

            if date_format == "iso_string":
                return list(map(lambda date: self.__query.convert_to_string().iso_format(date), out))

            if date_format == "investing_string":
                return list(map(lambda date: self.__query.convert_to_string().investing_format(date), out))

            return out

        @DeprecationWarning
        def __get_dates_array_for_dataset(self):
            """
            Unused
            :return:
            dates array
            """

            first_date = None

            for date in self.__query.get_dates_array(date_format="iso_string"):

                try:
                    temp = self.__stock_data.raw_data['Close'][date]
                    first_date = date
                except KeyError:
                    continue
                else:
                    print(first_date)
                    break
            interval = self.__get_date_interval_in_dataset(first_date)
            dates_array = []

            n = 0
            first_date = datetime.datetime.date(datetime.datetime.strptime(first_date, "%Y-%m-%d"))
            while first_date + n * interval < self.__query.end_date:
                dates_array.append(datetime.date.strftime(first_date + n * interval, "%Y-%m-%d"))
                n += 1

            return dates_array

        def __get_date_interval_in_dataset(self, first_date):

            first_date = datetime.datetime.strptime(first_date, "%Y-%m-%d")
            interval = datetime.timedelta(days=1)

            try:
                temp = self.__stock_data.raw_data['Close'][datetime.date.strftime(first_date + interval, "%Y-%m-%d")]
                return interval
            except KeyError:
                interval = datetime.timedelta(days=7)

            try:
                temp = self.__stock_data.raw_data['Close'][datetime.date.strftime(first_date + interval, "%Y-%m-%d")]
                return interval
            except KeyError:
                interval = datetime.timedelta(days=30)

            try:
                temp = self.__stock_data.raw_data['Close'][datetime.date.strftime(first_date + interval, "%Y-%m-%d")]
                return interval
            except KeyError:
                print("Unknown interval")
                return None
