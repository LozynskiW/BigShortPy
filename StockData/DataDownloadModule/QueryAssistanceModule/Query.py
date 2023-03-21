import datetime
import warnings


class Query:
    """

    |<-end_date ------------------------------------ start_date ->|
    |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
       past                                                  today   time ->
    """

    def __init__(self, start_date=datetime.date.today(),
                 end_date=datetime.date.today() - datetime.timedelta(days=30),
                 company="company",
                 country="country"
                 ):

        self.__start_date = start_date
        self.__end_date = end_date
        self.__company = company
        self.__country = country

    @property
    def end_date(self):
        return self.__end_date

    @property
    def start_date(self):
        return self.__start_date

    @property
    def company(self):
        return self.__company

    @property
    def country(self):
        return self.__country

    @start_date.setter
    def start_date(self, start_date):

        if type(start_date) is not datetime.date:
            raise ValueError("Date type must be datetime")

        self.__start_date = start_date

    @end_date.setter
    def end_date(self, end_date):

        if not end_date:
            raise ValueError("First choose start time")
        if type(end_date) is not datetime.date:
            raise ValueError("Date type must be datetime.date")

        self.__end_date = end_date

    @company.setter
    def company(self, company):
        if type(company) is not str:
            raise ValueError("Company must be a string value")
        self.__company = company

    @country.setter
    def country(self, country):
        if type(country) is not str:
            raise ValueError("Company must be a string value")
        self.__country = country

    def convert_to_string(self):
        return self.ToString

    def get_dates_array(self, date_format="datetime"):
        """
        Using this method shows all dates in query which means all days from start to end.
        If You meant only days when stock market was open (which is probably what You wanted) then
        consider using to_dates_array from stock_data class
        :param date_format: format in which dates in output array are going to be returned
        :return:
        """
        out = []

        for d in range(0, (self.end_date - self.start_date).days + 1):
            out.append(self.start_date + datetime.timedelta(days=d))

        if date_format == "iso_string":
            return list(map(lambda date: self.convert_to_string().iso_format(date), out))

        if date_format == "investing_string":
            return list(map(lambda date: self.convert_to_string().investing_format(date), out))

        return out

    class ToString:

        @staticmethod
        def investing_format(date: datetime.date):
            return datetime.date.strftime(date, "%d/%m/%Y")

        @staticmethod
        def iso_format(date: datetime.date):
            return datetime.date.strftime(date, "%Y-%m-%d")