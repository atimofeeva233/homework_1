def filter_by_state(list_dict, state="EXECUTED"):
    """
    Функция, возвращающая новый список словарей, содержащих только те словари,
    у которых ключ соответствует state
    :param list_dict:
        list_dict(list): Словари, состоящие из id, state, date
    :param state:
        state (str): Ключ, по которому будем выбирать
    :return:
        Список словарей: Словарь, отфильтрованный по ключу state
    """
    new_list = []
    for dicts in list_dict:
        if dicts["state"] == state:
            new_list.append(dicts)

    return new_list


def sor_by_date(list_dict, reverse: bool = True):
    """
    Функция, возвращающая новый список, отсортированный по дате
    :param list_dict:
        list_dict(list): Словари, состоящие из id, state, date
    :param reverse:
        reverse (bool): Значение для сортировки (по умол. - убывающее)
    :return:
        Новый, отсортированный по дате список
    """
    return sorted(list_dict, key=lambda x: x["date"], reverse=reverse)
