import datetime

import pandas


def date_from_string(date: str, format='iso'):
    if format == 'iso':
        return datetime.datetime.strptime(date, "%Y-%m-%d")
    elif format == 'investing':
        return datetime.datetime.strptime(date, "%d/%m/%Y")
    else:
        return datetime.datetime.strptime(date, "%d.%m.%Y")


def investing_format(date: datetime.date):
    return datetime.date.strftime(date, "%d/%m/%Y")


def iso_format(date: datetime.date):
    return datetime.date.strftime(date, "%Y-%m-%d")


def panda_to_dict(pandas_data):
    if type(pandas_data) is not pandas.core.frame.DataFrame:
        raise ValueError('Provided data must be in pandas.core.frame.DataFrame format')

    return pandas_data.to_json(date_format='iso', compression='dict', orient="index")


