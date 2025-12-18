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
    clean_number = ''.join(filter(str.isalpha, type_number_card))
    if clean_number == 'Счет':
        number = "".join(filter(str.isdigit, type_number_card))

        if len(number) != 20:
            raise ValueError("Номер счета должен содержать 20 цифр")

        masked_number = f"Счет **{number[-4:]}"

        return masked_number

    else:
        number = "".join(filter(str.isdigit, type_number_card))

        if len(number) != 16:
            raise ValueError("Номер карты должен содержать 16 цифр")

        masked_number = f"{clean_number} {number[:4]} {number[4:6]}** **** {number[-4:]}"

        return masked_number


def get_date(data) -> str:
    """
     Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Args:
        data: Дата в формате ISO (например: "2024-03-11T02:26:18.671407")

    Returns:
        str: Дата в формате ДД.ММ.ГГГГ
    """
    if data != '':
        number = "".join(filter(str.isdigit, data[:10]))
        mask_data = f'{number[-2:]}.{number[-4: -2]}.{number[:4]}'
        return mask_data
    return 0
