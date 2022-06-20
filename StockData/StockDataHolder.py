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

        self.__data['daily'] = self.__download_data().daily()

        if (self.__query.end_date - self.__query.start_date).days > 7:
            self.__data['weekly'] = self.__download_data().weekly()

        if (self.__query.end_date - self.__query.start_date).days > 30:
            self.__data['monthly'] = self.__download_data().monthly()

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

    def get_dates_arrays_dict(self, date_format="datetime"):
        "From oldest to newest"

        dates_dict = {}

        for interval in ['daily', 'weekly', 'monthly']:

            out = []

            for d in self.query.get_dates_array(date_format='iso_string'):

                try:
                    temp = self.data[interval]['Close'][d]
                    out.append(datetime.datetime.strptime(d, "%Y-%m-%d").date())
                except KeyError:
                    continue

            if date_format == "iso_string":
                out = list(map(lambda date: self.__query.convert_to_string().iso_format(date), out))

            if date_format == "investing_string":
                out = list(map(lambda date: self.__query.convert_to_string().investing_format(date), out))

            dates_dict[interval] = out

        return dates_dict

    def convert(self):
        return self.__Convert(self, self.__query)

    def get_data(self, start_date=None, end_date=None):

        if start_date is None:
            start_date = self.__query.start_date

        if end_date is None:
            end_date = self.__query.end_date

        if type(start_date) != datetime.date or type(end_date) != datetime.date:
            raise ValueError("Invalid date format, must be in datetime.date")

        if start_date < self.__query.start_date or end_date > self.__query.end_date:
            raise ValueError("Given dates exceed dates span in query, set query with higher dates span, ",
                             "start_date: ", self.__query.start_date,
                             "end_date: ", self.__query.end_date)

        return self.__DataGiveaway(self,
                                   dates_array=self.get_dates_arrays_dict(),
                                   start_date=start_date,
                                   end_date=end_date)

    def __download_data(self):
        return self.__DataDownload(self.__data_source, self.__query)

    class __DataGiveaway:

        def __init__(self, data, dates_array, start_date, end_date):
            self.__raw_data = data.data
            self.__dates_array = dates_array
            self.__start_date = start_date
            self.__end_date = end_date

        def dict(self):
            return self.__Dict(pandas_data=self.__raw_data,
                               dates_array=self.__dates_array,
                               start_date=self.__start_date,
                               end_date=self.__end_date)

        class __Dict:

            def __init__(self, pandas_data, dates_array, start_date, end_date):
                self.__pandas_data = pandas_data
                self.__dates_array = dates_array
                self.__start_date = start_date
                self.__end_date = end_date

            def __to_dict(self, pandas_data, interval=None):

                if type(pandas_data) is not pandas.core.frame.DataFrame:
                    raise ValueError('Provided data must be in pandas.core.frame.DataFrame format')

                data_dict = {}
                index = 0

                for d in self.__dates_array[interval]:

                    if self.__start_date <= d <= self.__end_date:

                        try:
                            data_dict[d] = [{
                                'Open': pandas_data['Open'][index],
                                'High': pandas_data['High'][index],
                                'Low': pandas_data['Low'][index],
                                'Close': pandas_data['Close'][index],
                                'Volume': pandas_data['Volume'][index],
                            }]

                        except KeyError:
                            continue
                    index += 1

                return data_dict

            def daily(self):
                return self.__to_dict(pandas_data=self.__pandas_data['daily'], interval='daily')

            def weekly(self):
                return self.__to_dict(pandas_data=self.__pandas_data['weekly'], interval='weekly')

            def monthly(self):
                return self.__to_dict(pandas_data=self.__pandas_data['monthly'], interval='monthly')

        class __Panda:

            def __init__(self, data):
                self.__data = data

            def daily(self):
                return self.__data['daily']

            def weekly(self):
                return self.__data['weekly']

            def monthly(self):
                return self.__data['monthly']

        class __NumpyArray:

            def __init__(self, pandas_data, dates_array):
                self.__pandas_data = pandas_data
                self.__dates_array = dates_array

            def to_np_array(self, series):
                "From oldest to newest"
                out = []

                for d in self.__stock_data.query.get_dates_array(date_format='iso_string'):

                    try:
                        out.append(self.__stock_data.raw_data[series][d])
                    except KeyError:
                        continue

                return out

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

        def to_np_array(self, series):
            "From oldest to newest"
            out = []

            for d in self.__stock_data.query.get_dates_array(date_format='iso_string'):

                try:
                    out.append(self.__stock_data.raw_data[series][d])
                except KeyError:
                    continue

            return out

        def to_dates_array(self, date_format="datetime"):
            "From oldest to newest"
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

        def divided_into_intervals(self, interval=7):
            """
            Method to calculate and return list of time intervals to calculate data
            return in form of [[from, to],[from, to]...]
            :return:
            """

            interval = self.__convert_interval(interval)

            time_intervals = []

            weeks_intervals = self.__calculate_weeks_intervals()

            weeks_intervals.reverse()

            num_of_weeks_intervals_in_time_interval = int(interval / 7)

            dict_data = self.__stock_data.get_data().dict().daily()

            for week in weeks_intervals:

                time_intervals.append([{'from': week[0],
                                        'to': week[1],
                                        'data': []
                                        }])

                for d in self.to_dates_array():

                    if week[0] <= d < week[1]:

                        time_intervals[-1][0]['data'].append(dict_data[d])

            return time_intervals

        def __convert_interval(self, interval):

            if interval in ['monthly', 'two_weeks', 14, 30]:
                raise ValueError("Not yet implemented")

            if interval == 'weekly' or interval == 7:
                return 7

            raise ValueError("Unsupported interval")

        def __calculate_weeks_intervals(self):
            """
            Method to calculate and return list of raw time intervals
            :return:
            """

            weeks_intervals = []

            day_num = self.__stock_data.query.start_date.isoweekday()

            # Select monday in week where query.start_date is
            week_start = self.__stock_data.query.start_date - datetime.timedelta(days=day_num - 1)
            # Select friday in week where query.start_date is
            week_end = self.__stock_data.query.start_date + datetime.timedelta(days=5 - day_num)

            week = [week_start, week_end]
            weeks_intervals.append(week)

            # Create a list where each element is date of weeks monday and friday
            # idea: [ [monday, friday],[monday, friday],[...] ]
            # example [ [datetime(28, 3, 2022), datetime(1, 4, 2022)],
            # [datetime(4, 4, 2022), datetime(8, 4, 2022)], [...] ]
            while self.__stock_data.query.end_date > week_start + datetime.timedelta(days=7):
                week_start = week_start + datetime.timedelta(days=7)
                week_end = week_end + datetime.timedelta(days=7)

                week = [week_start, week_end]
                weeks_intervals.append(week)

            return weeks_intervals

        @DeprecationWarning
        def __get_dates_array_for_dataset(self):
            """
            Unused
            :return:
            dates array
            """

            first_date = None

            for date in self.__query.get_dates_arrays_dict(date_format="iso_string"):

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
