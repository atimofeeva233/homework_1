def get_mask_card_number(card_number: str):
    """
    Функция маскирует номер карты в формате ХХХХ ХХ** **** ХХХХ

    Args:
        card_number (str): Номер карты (16 цифр)

    :return:
        str: Замаскированный номер карты
    """

    clean_number = "".join(filter(str.isdigit, card_number))

    if len(clean_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    masked_number = f"{clean_number[:4]} {clean_number[4:6]}** **** {clean_number[-4:]}"

    return masked_number


def get_mask_account(number_account: str):
    """
    Функция принимает номер счета и возвращает его маску в формате **XXXX

    Args:
        number_account (str): Номер счета  (20 цифр)

    :return:
        str: Замаскированный номер счета
    """

    clean_number = "".join(filter(str.isdigit, number_account))

    if len(clean_number) != 20:
        raise ValueError("Номер счета должен содержать 20 цифр")

    masked_number = f"**{clean_number[-4:]}"

    return masked_number
