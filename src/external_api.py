import os

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_to_rubles(transaction: dict) -> float:
    '''
    Конвертирует сумму транзакции в рубли.

    Если валюта RUB - возвращает сумму как есть.
    Если валюта USD или EUR - конвертирует через API.

    :param transaction: Словарь с данными транзакции

    :return: Сумма в рублях.
    '''

    # Получаем переменные из .env
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")

    # Получаем сумму и валюту из транзакции
    amount_str = transaction["operationAmount"]["amount"]
    currency = transaction["operationAmount"]["currency"]["code"].upper()

    # Преобразуем в число
    amount = float(amount_str)

    # Если валюта рубли - возвращаем как есть
    if currency == 'RUB':
        return round(amount, 2)

    # Для USD и EUR получаем курс через API
    elif currency in ['USD', 'EUR']:
        try:
            api_key = api_key

            # Делаем запрос к API
            url = 'https://api.apilayer.com/exchangerates_data/convert'

            params = {
                'from': currency,
                'to': 'RUB',
                'amount': amount
            }

            headers = {'apikey': api_key}

            # Пробуем получить курс

            response = requests.get(url, params=params, headers=headers)
            data = response.json()

            rate = data['result']

            result = amount * rate
            return round(result, 2)

        except Exception as e:
            print(f'API ошибка {e}')

    else:
        raise ValueError(f'Не могу конвертировать валюту: {currency}')
