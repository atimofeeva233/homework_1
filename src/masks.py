from src.logger_masks import setup_masks_logger

masks_logger = setup_masks_logger()


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
    masks_logger.info('Начало маскирования номера карты')

    try:
        masks_logger.debug(f'Входные данные: {card_number[:4]}***...')
        clean_number = "".join(filter(str.isdigit, card_number))

        if not clean_number:
            error_msg = "Номер карты не содержит цифр"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        if len(clean_number) != 16:
            error_msg = f"Номер карты должен содержать 16 цифр, получено {len(clean_number)}"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        masked_number = f"{clean_number[:4]} {clean_number[4:6]}** **** {clean_number[-4:]}"
        masks_logger.info(f"Успешно замаскирован номер карты: {masked_number}")

        return masked_number

    except ValueError as e:
        masks_logger.error(f"Ошибка валидации номера карты: {e}")
        raise
    except Exception as e:
        masks_logger.exception(f"Неожиданная ошибка при маскировании номера карты: {e}")
        raise


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
    masks_logger.info('Начало маскирования номера счета')
    try:
        # Логируем входящие данные (безопасно)
        masks_logger.debug(f'Входные данные: ...{number_account[-4:] if len(number_account) >= 4 else '***'}')
        clean_number = "".join(filter(str.isdigit, number_account))

        if not clean_number:
            error_msg = "Номер счета не содержит цифр"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        if len(clean_number) != 20:
            masks_logger.warning(f"Номер счета имеет нестандартную длину: {len(clean_number)} (ожидалось 20)")

        masked_number = f"**{clean_number[-4:]}"

        return masked_number

    except ValueError as e:
        masks_logger.error(f"Ошибка валидации номера счета: {e}")
        raise
    except Exception as e:
        masks_logger.exception(f"Неожиданная ошибка при маскировании номера счета: {e}")
        raise
