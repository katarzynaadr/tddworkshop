import json
import requests

class UnsupportedExchangeRateError(Exception):
    """Exception raised when there's not enough data to preform exchange"""
    pass


class CurrencyExchanger(object):
    def __init__(self, exchange_rates=None, default_currency=None):
        self.exchange_rates = exchange_rates
        self.default_currency = default_currency

    def exchange(self, value, input_currency, output_currency=None):
        output_currency = output_currency or self.default_currency

        if input_currency == output_currency:
            return value

        if not output_currency:
            raise UnsupportedExchangeRateError('Brak waluty wyjsciowej i domyslnej')

        exchange_rate = self.exchange_rates.get(
            (input_currency, output_currency)
        )

        if exchange_rate is None:
            raise UnsupportedExchangeRateError('Brak takiego kursu')

        if isinstance(exchange_rate, str) or isinstance(value, str):
            raise UnsupportedExchangeRateError('przelicznik/ilosc nie jest liczba')

        if value < 0:
            raise UnsupportedExchangeRateError('wartosc jest ujemna')

        return exchange_rate * value


class OnlineRates(object):

    def __init__(self, src=None):
        self.src = src

    def get_data(self):
        rates = json.loads(requests.get(self.src))
        return rates
