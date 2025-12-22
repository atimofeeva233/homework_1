import os
from unittest.mock import patch, MagicMock
import pytest
import requests
from src.external_api import convert_to_rubles


def test_convert_to_rubles_rub_currency():
    """Тест конвертации RUB валюты (без конвертации)"""
    transaction = {
        "operationAmount": {
            "amount": "1500.50",
            "currency": {
                "code": "RUB"
            }
        }
    }

    result = convert_to_rubles(transaction)

    assert result == 1500.50
    assert isinstance(result, float)


def test_convert_to_rubles_usd_currency_success():
    """Тест успешной конвертации USD в RUB через API"""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }

    # Мокаем ответ API
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 92.50}

    with patch('os.getenv', return_value='test_api_key'), \
            patch('requests.get', return_value=mock_response) as mock_get:
        result = convert_to_rubles(transaction)

        # Проверяем вызов API
        mock_get.assert_called_once_with(
            'https://api.apilayer.com/exchangerates_data/convert',
            params={'from': 'USD', 'to': 'RUB', 'amount': 100.0},
            headers={'apikey': 'test_api_key'}
        )

        assert result == 9250.0
        assert isinstance(result, float)


def test_convert_to_rubles_eur_currency_success():
    """Тест успешной конвертации EUR в RUB через API"""
    transaction = {
        "operationAmount": {
            "amount": "50.75",
            "currency": {
                "code": "EUR"
            }
        }
    }

    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 99.30}

    with patch('os.getenv', return_value='test_api_key'), \
            patch('requests.get', return_value=mock_response) as mock_get:
        result = convert_to_rubles(transaction)

        mock_get.assert_called_once_with(
            'https://api.apilayer.com/exchangerates_data/convert',
            params={'from': 'EUR', 'to': 'RUB', 'amount': 50.75},
            headers={'apikey': 'test_api_key'}
        )

        assert result == 5039.47


def test_convert_to_rubles_api_error():
    """Тест обработки ошибки API"""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }

    with patch('os.getenv', return_value='test_api_key'), \
            patch('requests.get', side_effect=requests.RequestException("Connection error")), \
            patch('builtins.print') as mock_print:

        # Функция должна вернуть None при ошибке API
        result = convert_to_rubles(transaction)

        assert result is None
        mock_print.assert_called_once_with('API ошибка Connection error')
