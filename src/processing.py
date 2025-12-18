def filter_by_state(list_dict, state="EXECUTED") -> list:
    """
    Фильтрует список транзакций по состоянию.

    Args:
        list_dict: Список словарей с транзакциями
        state: Состояние для фильтрации (по умолчанию "EXECUTED")

    Returns:
        List[Dict]: Список словарей, отфильтрованный по ключу state
    """
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

    Note:
        Использует стабильную сортировку. При одинаковых датах сохраняется исходный порядок.
    """
    return sorted(list_dict, key=lambda x: x["date"], reverse=reverse)
