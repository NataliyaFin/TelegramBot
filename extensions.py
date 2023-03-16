import requests
import json
from config import keys, API_KEY


class ConvertionException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}.')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={quote_ticker}&from={base_ticker}&amount={amount}"
        payload = {}
        headers = {"apikey": API_KEY}
        r = requests.request("GET", url, headers=headers, data=payload)
        resp = json.loads(r.content)
        total_base = resp['result']

        return round(total_base, 3)
