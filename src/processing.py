def filter_by_state(list_dict, state="EXECUTED") -> list:
    """
    Фильтрует список транзакций по состоянию.

    Args:
        list_dict: Список словарей с транзакциями
        state: Состояние для фильтрации (по умолчанию "EXECUTED")

    Returns:
        List[Dict[str, Any]]: Список словарей, отфильтрованный по ключу state

    Raises:
        TypeError: Если входные данные не являются списком
        ValueError: Если список пуст или состояние не поддерживается
    """
    if not isinstance(list_dict, list):
        raise TypeError(f"Ожидается список, получено {type(list_dict).__name__}")

    if not list_dict:
        raise ValueError("Список транзакций не может быть пустым")

        # Поддерживаемые состояния
    valid_states = {"EXECUTED", "CANCELED", "PENDING", "FAILED"}
    if state not in valid_states:
        raise ValueError(
            f"Неподдерживаемое состояние: {state}. "
            f"Допустимые значения: {', '.join(sorted(valid_states))}"
        )
    new_list = []
    for dicts in list_dict:
        if dicts["state"] == state:
            new_list.append(dicts)

    return new_list


def sort_by_date(list_dict, reverse: bool = True) -> list:
    """
    Сортирует список транзакций по дате.

    Args:
        list_dict: Список словарей с транзакциями
        reverse: Если True - сортировка по убыванию, False - по возрастанию

    Returns:
        List[Dict]: Отсортированный по дате список транзакций

    Raises:
        TypeError: Если входные данные не являются списком
        ValueError: Если список пуст или содержит некорректные данные
        KeyError: Если в транзакции отсутствует ключ 'date'

    Note:
        Использует стабильную сортировку. При одинаковых датах сохраняется исходный порядок.
    """
    if not isinstance(list_dict, list):
        raise TypeError(f"Ожидается список, получено {type(list_dict).__name__}")

    if not list_dict:
        raise ValueError("Список транзакций не может быть пустым")
    return sorted(list_dict, key=lambda x: x["date"], reverse=reverse)
