import datetime
from .util import investing_format, iso_format, date_from_string


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

        if type(start_date) is str:

            try:
                start_date = date_from_string(start_date)
            except Exception:
                raise ValueError("500")

        self.__start_date = start_date

    @end_date.setter
    def end_date(self, end_date):

        if not end_date:
            raise ValueError("First choose start time")

        if type(end_date) is str:

            try:
                end_date = date_from_string(end_date)

            except Exception:
                raise ValueError("500")

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