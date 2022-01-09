class BasicMemory:

    def __init__(self):
        self.__historic_decisions = []

    def add_new_transaction(self, position_opening_day, instrument_price, position_type, instrument):
        self.__historic_decisions.append({
            "instrument": instrument,
            "open_day": position_opening_day,
            "close_day": None,
            "start_price": instrument_price,
            "end_price": None,
            "type": position_type,
            "isClosed": False
        })

    def get_all_currently_opened_transactions(self):
        return list(map(lambda i: i["isClosed"] is False, self.__historic_decisions))

    def get_transactions_history(self):
        return self.__historic_decisions

    def close_transaction(self, open_day, instrument, close_day, end_price):
        transaction = filter(lambda i: i["open_day"] is open_day and i["instrument"] is instrument, self.__historic_decisions)

        transaction["close_day"] = close_day
        transaction["end_price"] = end_price
        transaction["isClosed"] = True

        self.__historic_decisions