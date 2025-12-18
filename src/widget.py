def mask_account_card(type_number_card) -> str:
    """
    Функция маскирует номер карты или номер счета

    :param type_number_card:
        type_number_card (str): Строка, содержащая тип и номер карты или счета

    :return:
        str: Замаскированный номер карты или счета
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
    Функция принимает дату в формате "2024-03-11T02:26:18.671407"
    и возвращает в формате "ДД.ММ.ГГГГ" ("11.03.2024")

    :param data:
        data(str): Формат даты "2024-03-11T02:26:18.671407"

    :return:
        str: Формат даты "ДД.ММ.ГГГГ" ("11.03.2024")
    """
    if data != '':
        number = "".join(filter(str.isdigit, data[:10]))
        mask_data = f'{number[-2:]}.{number[-4: -2]}.{number[:4]}'
        return mask_data
    return 0
