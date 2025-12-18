def get_mask_card_number(card_number: str) -> str:
    """
     Маскирует номер карты в формате XXXX XX** **** XXXX.

    Args:
        card_number: Номер карты (16 цифр), может содержать пробелы

    Returns:
        str: Замаскированный номер карты в формате XXXX XX** **** XXXX

    Raises:
        ValueError: Если номер карты содержит не 16 цифр
    """

    clean_number = "".join(filter(str.isdigit, card_number))

    if len(clean_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    masked_number = f"{clean_number[:4]} {clean_number[4:6]}** **** {clean_number[-4:]}"

    return masked_number


def get_mask_account(number_account: str) -> str:
    """
    Маскирует номер счета в формате **XXXX.

    Args:
        number_account: Номер счета (20 цифр), может содержать пробелы

    Returns:
        str: Замаскированный номер счета в формате **XXXX

    Raises:
        ValueError: Если номер счета содержит меньше 4 цифр
    """

    clean_number = "".join(filter(str.isdigit, number_account))

    if len(clean_number) != 20:
        raise ValueError("Номер счета должен содержать 20 цифр")

    masked_number = f"**{clean_number[-4:]}"

    return masked_number
