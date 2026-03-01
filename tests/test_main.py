import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from main import (FILE_PATHS, format_transaction, get_sort_order, get_yes_no,
                  load_transactions)

# Добавляем корневую папку в путь импорта
sys.path.insert(0, str(Path(__file__).parent.parent))


# ============= ТЕСТЫ ДЛЯ get_yes_no =============

@pytest.mark.parametrize("user_input,expected", [
    ("да", True),
    ("Да", True),
    ("ДА", True),
    ("yes", True),
    ("YES", True),
    ("y", True),
    ("Y", True),
    ("нет", False),
    ("Нет", False),
    ("НЕТ", False),
    ("no", False),
    ("NO", False),
    ("n", False),
    ("N", False),
])
def test_get_yes_no_valid(monkeypatch, user_input, expected):
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    assert get_yes_no("Тестовый вопрос") == expected


def test_get_yes_no_invalid_then_valid(monkeypatch, capsys):
    inputs = iter(["может быть", "да"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    result = get_yes_no("Тестовый вопрос")
    captured = capsys.readouterr()

    assert '\nПрограмма: Пожалуйста, введите "Да" или "Нет"' in captured.out
    assert result is True


# ============= ТЕСТЫ ДЛЯ get_sort_order =============

@pytest.mark.parametrize("user_input,expected", [
    ("возрастанию", "возрастанию"),
    ("убыванию", "убыванию"),
    ("asc", "возрастанию"),
    ("desc", "убыванию"),
])
def test_get_sort_order_valid(monkeypatch, user_input, expected):
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    assert get_sort_order() == expected


def test_get_sort_order_invalid_then_valid(monkeypatch, capsys):
    inputs = iter(["по дате", "возрастанию"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    result = get_sort_order()
    captured = capsys.readouterr()

    assert '\nПрограмма: Пожалуйста, введите "по возрастанию" или "по убыванию"' in captured.out
    assert result == "возрастанию"


# ============= ТЕСТЫ ДЛЯ format_transaction =============

def test_format_transaction_with_from_and_to_rub():
    transaction = {
        "date": "2019-08-26T10:50:58.294041",
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {"code": "RUB"}
        }
    }

    result = format_transaction(transaction)
    assert "26.08.2019 Перевод организации" in result
    assert "Maestro 1596837868705199 -> Счет 64686473678894779589" in result
    assert "Сумма: 31957.58 руб." in result


def test_format_transaction_without_from():
    transaction = {
        "date": "2018-03-23T10:45:06.972075",
        "description": "Открытие вклада",
        "to": "Счет 41421565395219882431",
        "operationAmount": {
            "amount": "48223.05",
            "currency": {"code": "RUB"}
        }
    }

    result = format_transaction(transaction)
    assert "23.03.2018 Открытие вклада" in result
    assert "Счет 41421565395219882431" in result
    assert "Сумма: 48223.05 руб." in result


# ============= ТЕСТЫ ДЛЯ load_transactions =============


@patch('main.get_test_data')
def test_load_transactions_csv(mock_get_test_data):
    """Тест загрузки из CSV (используются тестовые данные)"""
    mock_get_test_data.return_value = [{"test": "test_data"}]

    result = load_transactions("2", "test.csv")

    assert result == [{"test": "test_data"}]


@patch('main.get_test_data')
def test_load_transactions_xlsx(mock_get_test_data):
    """Тест загрузки из XLSX (используются тестовые данные)"""
    mock_get_test_data.return_value = [{"test": "test_data"}]

    result = load_transactions("3", "test.xlsx")

    assert result == [{"test": "test_data"}]


@patch('main.load_trans_from_json')
@patch('main.get_test_data')
def test_load_transactions_json_error(mock_get_test_data, mock_load_json):
    """Тест ошибки при загрузке JSON"""
    mock_load_json.side_effect = Exception("Test error")
    mock_load_json.__name__ = 'load_trans_from_json'
    mock_get_test_data.return_value = [{"test": "test_data"}]

    result = load_transactions("1", "test.json")

    # Проверяем, что вернулись тестовые данные
    assert result == [{"test": "test_data"}]


