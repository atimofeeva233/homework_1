def mask_account_card(type_number_card) -> str:
    """
    Маскирует номер карты или номер счета в зависимости от типа.

    Args:
        type_number_card: Строка, содержащая тип и номер карты или счета
                         (например: "Visa 1234567890123456" или "Счет 12345678901234567890")

    Returns:
        str: Замаскированный номер карты или счета с указанием типа

    Raises:
        ValueError: Если тип не распознан или номер некорректен
    """
    if not isinstance(type_number_card, str):
        raise TypeError(f"Ожидается строка, получено {type(type_number_card).__name__}")

    if not type_number_card.strip():
        raise ValueError("Пустая строка не может быть обработана")

        # Разделяем тип и номер
    parts = type_number_card.split()
    if len(parts) < 2:
        raise ValueError(f"Некорректный формат: {type_number_card}. Ожидается 'Тип Номер'")

    card_type = parts[0]
    number_str = "".join(parts[1:])  # Объединяем все остальные части (на случай пробелов в номере)

    # Проверяем, что номер содержит только цифры
    if not number_str.isdigit():
        raise ValueError(f"Номер должен содержать только цифры: {number_str}")

    number = number_str

    if card_type == 'Счет':
        if len(number) != 20:
            raise ValueError(f"Номер счета должен содержать 20 цифр, получено {len(number)}: {number}")

        masked_number = f"Счет **{number[-4:]}"
        return masked_number

    else:  # Карта
        if len(number) != 16:
            raise ValueError(f"Номер карты должен содержать 16 цифр, получено {len(number)}: {number}")

        # Форматируем номер карты: XXXX XX** **** XXXX
        masked_number = f"{card_type} {number[:4]} {number[4:6]}** **** {number[-4:]}"
        return masked_number


def get_date(data) -> str:
    """
     Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Args:
        date_str: Дата в формате ISO (например: "2024-03-11T02:26:18.671407")

    Returns:
        str: Дата в формате ДД.ММ.ГГГГ

    Raises:
        ValueError: Если строка пустая или некорректного формата
        TypeError: Если передан не строковый тип
    """
    if data is None:
        raise ValueError("Дата не может быть None")

    if not isinstance(data, str):
        raise TypeError(f"Ожидается строка, получено {type(data).__name__}")

    if not data.strip():
        raise ValueError("Пустая строка не может быть преобразована")
    number = "".join(filter(str.isdigit, data[:10]))
    mask_data = f'{number[-2:]}.{number[-4: -2]}.{number[:4]}'
    return mask_data
