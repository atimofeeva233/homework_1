import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    '''
    Фильтрует список транзакций по наличию строки поиска в описании.

    :param data: Список словарей с данными о банковских операциях
    :param search: Строка для поиска в описании

    :return: list[dict]: Отфильтрованный список транзакций
    '''
    if not data or not search:
        return data if not search else []

    # Используем регулярное выражение (регистронезависимый поиск)
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    return [
        t for t in data
        if isinstance(t.get('description', ''), str)
        and pattern.search(t.get('description', ''))
    ]


def process_bank_operations(data: list[dict], categories: list) -> dict:
    '''
    Подсчитывает количество транзакций в каждой категории.

    :param data: Список словарей с данными о банковских операциях
    :param categories: Список названий категориий для подсчета

    :return: dict: Словарь с количеством транзакций по категориям
    '''
    if not categories:
        return {}

    if not data:
        return {category: 0 for category in categories}

    # Создаем список категорий для каждой транзакции
    transaction_categories = []

    for transaction in data:
        description = transaction.get("description", "")

        if not isinstance(description, str):
            continue

        # Проверяем, к каким категориям относится транзакция
        for category in categories:
            try:
                # Используем регулярное выражение для поиска категории в описании
                pattern = re.compile(re.escape(category), re.IGNORECASE)
                if pattern.search(description):
                    transaction_categories.append(category)
                    # Не делаем break, чтобы транзакция могла попасть в несколько категорий
            except Exception:
                continue

        # Используем Counter для подсчета
    counter = Counter(transaction_categories)

    # Формируем результат, включая все запрошенные категории (даже с нулевым количеством)
    result = {category: counter.get(category, 0) for category in categories}

    return result
