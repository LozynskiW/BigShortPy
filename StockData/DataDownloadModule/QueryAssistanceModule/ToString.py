import datetime


def investing_format(date: datetime.date):
    return datetime.date.strftime(date, "%d/%m/%Y")


def iso_format(date: datetime.date):
    return datetime.date.strftime(date, "%Y-%m-%d")
