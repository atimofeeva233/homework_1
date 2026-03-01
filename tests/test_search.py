import pytest
from src.search import process_bank_operations, process_bank_search


def test_process_bank_search_basic():
    """Тест базового поиска по описанию"""
    transactions = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод с карты на карту"},
        {"id": 3, "description": "Оплата услуг"},
        {"id": 4, "description": "Покупка в магазине"},
    ]

    result = process_bank_search(transactions, "Перевод")

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2
    assert all("Перевод" in t["description"] for t in result)


def test_process_bank_search_case_insensitive():
    """Тест регистронезависимости поиска"""
    transactions = [
        {"id": 1, "description": "ПЕРЕВОД организации"},
        {"id": 2, "description": "перевод с карты"},
        {"id": 3, "description": "Перевод на карту"},
        {"id": 4, "description": "Оплата услуг"},
    ]

    # Поиск в нижнем регистре
    result_lower = process_bank_search(transactions, "перевод")
    assert len(result_lower) == 3

    # Поиск в верхнем регистре
    result_upper = process_bank_search(transactions, "ПЕРЕВОД")
    assert len(result_upper) == 3

    # Поиск смешанного регистра
    result_mixed = process_bank_search(transactions, "ПеРеВоД")
    assert len(result_mixed) == 3


def test_process_bank_search_no_matches():
    """Тест когда нет совпадений"""
    transactions = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Оплата услуг"},
    ]

    result = process_bank_search(transactions, "Снятие")
    assert result == []


def test_process_bank_search_empty_transactions():
    """Тест с пустым списком транзакций"""
    result = process_bank_search([], "Перевод")
    assert result == []


def test_process_bank_search_empty_search():
    """Тест с пустой строкой поиска"""
    transactions = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Оплата услуг"},
    ]

    result = process_bank_search(transactions, "")
    assert result == transactions  # Должен вернуть все транзакции


def test_process_bank_search_with_special_chars():
    """Тест поиска строк со спецсимволами"""
    transactions = [
        {"id": 1, "description": "Перевод (срочный)"},
        {"id": 2, "description": "Оплата [интернет]"},
        {"id": 3, "description": "Покупка *маркет*"},
    ]

    result1 = process_bank_search(transactions, "(срочный)")
    assert len(result1) == 1
    assert result1[0]["id"] == 1

    result2 = process_bank_search(transactions, "[интернет]")
    assert len(result2) == 1
    assert result2[0]["id"] == 2

    result3 = process_bank_search(transactions, "*маркет*")
    assert len(result3) == 1
    assert result3[0]["id"] == 3


def test_process_bank_search_missing_description():
    """Тест транзакций без поля description"""
    transactions = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Оплата услуг"},
        {"id": 3},  # нет description
        {"id": 4, "description": None},  # description = None
        {"id": 5, "description": 12345},  # description не строка
    ]

    result = process_bank_search(transactions, "Перевод")

    assert len(result) == 1
    assert result[0]["id"] == 1


def test_process_bank_search_partial_match():
    """Тест частичного совпадения"""
    transactions = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Переводчик услуг"},  # содержит "Перевод" как часть слова
        {"id": 3, "description": "Оплата перевода"},
    ]

    result = process_bank_search(transactions, "Перевод")

    assert len(result) == 3  # Должны найтись все, т.к. "Перевод" есть везде


def test_process_bank_operations_basic():
    """Тест базового подсчета по категориям"""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
        {"description": "Оплата услуг"},
        {"description": "Перевод организации"},
        {"description": "Покупка в магазине"},
        {"description": "Снятие наличных"},
    ]

    categories = ["Перевод", "Оплата", "Покупка", "Снятие"]

    result = process_bank_operations(transactions, categories)

    assert result == {
        "Перевод": 3,
        "Оплата": 1,
        "Покупка": 1,
        "Снятие": 1
    }


def test_process_bank_operations_case_insensitive():
    """Тест регистронезависимости при подсчете"""
    transactions = [
        {"description": "ПЕРЕВОД организации"},
        {"description": "перевод с карты"},
        {"description": "Перевод на карту"},
        {"description": "ОПЛАТА услуг"},
        {"description": "оплата интернета"},
    ]

    categories = ["Перевод", "Оплата"]

    result = process_bank_operations(transactions, categories)

    assert result == {
        "Перевод": 3,
        "Оплата": 2
    }


def test_process_bank_operations_no_matches():
    """Тест когда нет совпадений ни с одной категорией"""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Оплата услуг"},
    ]

    categories = ["Снятие", "Покупка"]

    result = process_bank_operations(transactions, categories)

    assert result == {
        "Снятие": 0,
        "Покупка": 0
    }


def test_process_bank_operations_empty_transactions():
    """Тест с пустым списком транзакций"""
    categories = ["Перевод", "Оплата"]

    result = process_bank_operations([], categories)

    assert result == {
        "Перевод": 0,
        "Оплата": 0
    }


def test_process_bank_operations_empty_categories():
    """Тест с пустым списком категорий"""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Оплата услуг"},
    ]

    result = process_bank_operations(transactions, [])

    assert result == {}


def test_process_bank_operations_missing_description():
    """Тест транзакций без поля description"""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Оплата услуг"},
        {"id": 3},  # нет description
        {"description": None},  # description = None
        {"description": 12345},  # description не строка
        {"description": "Перевод с карты"},
    ]

    categories = ["Перевод", "Оплата"]

    result = process_bank_operations(transactions, categories)

    # Должны учесть только первые две и последнюю транзакции
    assert result == {
        "Перевод": 2,  # "Перевод организации" и "Перевод с карты"
        "Оплата": 1  # "Оплата услуг"
    }


def test_process_bank_operations_multiple_categories_per_transaction():
    """Тест когда транзакция подходит под несколько категорий"""
    transactions = [
        {"description": "Перевод организации"},  # только Перевод
        {"description": "Оплата перевода"},  # Оплата и Перевод
        {"description": "Покупка с переводом"},  # Покупка и Перевод
        {"description": "Снятие наличных"},  # только Снятие
    ]

    categories = ["Перевод", "Оплата", "Покупка", "Снятие"]

    result = process_bank_operations(transactions, categories)

    # Транзакция может учитываться в нескольких категориях
    assert result == {
        "Перевод": 3,  # есть в первых трех транзакциях
        "Оплата": 1,  # есть во второй транзакции
        "Покупка": 1,  # есть в третьей транзакции
        "Снятие": 1  # есть в четвертой транзакции
    }


def test_process_bank_operations_with_special_chars():
    """Тест категорий со спецсимволами"""
    transactions = [
        {"description": "Перевод (срочный)"},
        {"description": "Оплата [интернет]"},
        {"description": "Покупка *маркет*"},
    ]

    categories = ["(срочный)", "[интернет]", "*маркет*"]

    result = process_bank_operations(transactions, categories)

    assert result == {
        "(срочный)": 1,
        "[интернет]": 1,
        "*маркет*": 1
    }


def test_process_bank_operations_partial_matches():
    """Тест частичных совпадений с категориями"""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Переводчик услуг"},  # содержит "Перевод" как часть слова
        {"description": "Оплата перевода"},
    ]

    categories = ["Перевод"]

    result = process_bank_operations(transactions, categories)

    # Должны найтись все, где есть подстрока "Перевод"
    assert result == {"Перевод": 3}


@pytest.mark.parametrize("transactions, search_string, expected_count", [
    ([{"description": "Перевод"}, {"description": "Оплата"}], "Перевод", 1),
    ([{"description": "ПЕРЕВОД"}, {"description": "перевод"}], "Перевод", 2),
    ([], "Перевод", 0), ])
def test_process_bank_search_parametrized(transactions, search_string, expected_count):
    """Параметризованные тесты для filter_by_description"""
    result = process_bank_search(transactions, search_string)
    assert len(result) == expected_count


@pytest.mark.parametrize("transactions, categories, expected", [
    ([{"description": "Перевод"}, {"description": "Перевод"}], ["Перевод", "Оплата"], {"Перевод": 2, "Оплата": 0}),
    ([{"description": "ПЕРЕВОД"}, {"description": "перевод"}], ["Перевод"], {"Перевод": 2}),
    ([], ["Перевод"], {"Перевод": 0})])
def test_process_bank_operations_parametrized(transactions, categories, expected):
    """Параметризованные тесты для count_by_categories"""
    result = process_bank_operations(transactions, categories)
    assert result == expected
