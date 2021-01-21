import os
from decimal import Decimal
import simplejson as json
import requests
from datetime import datetime


class RatesNotAvailableErr(Exception):
    pass


class DecimalFloatMismatchErr(Exception):
    pass


class GetData:

    def __init__(self, force_decimal=False):
        self._force_decimal = force_decimal

    def _get_date_string(self, date_obj):
        if date_obj is None:
            return 'latest'
        try:
            date_str = datetime.strptime(date_obj, '%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            date_str = datetime.strptime(date_obj, '%d-%m-%Y').strftime('%d-%m-%Y')
        return date_str

    def _decode_rates(self, response, jsonLocation, use_decimal=False):
        if self._force_decimal or use_decimal:
            decoded_data = json.loads(response.text, use_decimal=True).get(jsonLocation, {})
        else:
            decoded_data = response.json().get(jsonLocation, {})
        return decoded_data

    def _get_decoded_rate(self, response, dest_cur, use_decimal=False):
        return self._decode_rates(response, use_decimal=use_decimal).get(dest_cur, None)


class CurrencyRates(GetData):

    def get_rates(self, source_url, date_obj=None, jsonLocation=None):
        date_str = self._get_date_string(date_obj)
        source_url = source_url.format(date_str)
        response = requests.get(source_url)
        if response.status_code == 200:
            rates = self._decode_rates(response, jsonLocation)
            return rates
        raise RatesNotAvailableErr("Currency Rates Source Not Ready")

    def get_best_rate(self, *args):
        eurLst = []
        usdLst = []
        for data in args:
            for key in data.keys():
                if "EUR" in key:
                    try:
                        if data[key] < 1:
                            pass
                    except:
                        eurLst.append(str(data[key]))
                if "USD" in key:
                    try:
                        if data[key] < 1:
                            pass
                    except:
                        usdLst.append(str(data[key]))

        minUsd = min(usdLst)
        minEur = min(eurLst)
        return minUsd, minEur


_CURRENCY_FORMATTER = CurrencyRates()

get_rates = _CURRENCY_FORMATTER.get_rates
get_best_rate = _CURRENCY_FORMATTER.get_best_rate
