def filter_by_currency(transactions: list[dict], currency: str) -> iter[dict]:
    """
    Фильтрует транзакции по валюте и возвращает итератор.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (например, 'USD', 'RUB')

    Yields:
        Словари транзакций, где валюта операции соответствует заданной
    """
    for transaction in transactions:
        if transactions == []:
            return 0
        try:
            # Безопасно получаем код валюты через цепочку get()
            transaction_currency = transaction.get('operationAmount', {}).get('currency', {}).get('code')
            if transaction_currency == currency:
                yield transaction
        except (AttributeError, TypeError):
            # Пропускаем транзакции с некорректной структурой
            continue


def transaction_descriptions(transactions: list[dict]) -> str:
    """
     Генератор, который возвращает описание каждой транзакции по очереди.

    Args:
        transactions: Список словарей с транзакциями

    Yields:
        Описание транзакции (строка) или None, если описание отсутствует
    """
    for transaction in transactions:
        # Извлекаем описание, если оно есть
        description = transaction.get('description')
        yield description


def card_number_generator(start: int = 1, end: int = 9999999999999999):
    """
        Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

        Args:
            start: Начальный номер карты (от 1 до 9999999999999999)
            end: Конечный номер карты (от start до 9999999999999999)

        Yields:
            Номер карты в формате XXXX XXXX XXXX XXXX

        Raises:
            ValueError: Если параметры выходят за допустимые пределы
        """
    # Проверка корректности параметров
    if not (1 <= start <= 9999999999999999):
        raise ValueError(f"start должен быть в диапазоне от 1 до 9999999999999999, получено: {start}")

    if not (1 <= end <= 9999999999999999):
        raise ValueError(f"end должен быть в диапазоне от 1 до 9999999999999999, получено: {end}")

    if start > end:
        raise ValueError(f"start ({start}) не может быть больше end ({end})")

    # Генерируем номера карт
    for number in range(start, end + 1):
        # Форматируем номер как строку с ведущими нулями
        card_str = str(number).zfill(16)

        # Разбиваем на группы по 4 цифры
        formatted = f"{card_str[0:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"

        yield formatted
