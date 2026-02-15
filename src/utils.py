import json
import os
from typing import Any, Dict, List

from src.logger_utils import setup_utils_logger

utils_logger = setup_utils_logger()


def load_trans_from_json(filepath: str) -> List[Dict[str, Any]]:
    '''
    Функция загружает транзакции  из JSON-файла

    :param filepath: путь до JSON-файла

    :return: List[Dict[str, Any]]: Список словарей с данными о транзакциях.
    Возвращает пустой список в случае ошибок.
    '''
    utils_logger.info(f"Начало загрузки транзакций из файла: {filepath}")
    try:
        # Проверяем существование файла
        if not os.path.exists(filepath):
            error_msg = f'Файл не найден: {filepath}'
            utils_logger.error(error_msg)
            print(error_msg)
            return []

        # Проверяем, что это файл, а не директория
        if not os.path.isfile(filepath):
            error_msg = f"Указанный путь не является файлом: {filepath}"
            utils_logger.error(error_msg)
            print(error_msg)
            return []

        # Проверяем размер файла
        if os.path.getsize(filepath) == 0:
            error_msg = f"Файл пустой: {filepath}"
            utils_logger.error(error_msg)
            print(error_msg)
            return []

        # Читаем файл
        utils_logger.debug(f"Чтение файла: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read().strip()

            data = json.loads(content)

            # Проверяем, что данные - это список
            if not isinstance(data, list):
                error_msg = f"JSON не содержит список на верхнем уровне: {filepath}"
                utils_logger.error(error_msg)
                print(error_msg)
                return []

            # Проверяем, что все элементы списка - словари
            invalid_items = []
            for i, item in enumerate(data):
                if not isinstance(item, dict):
                    invalid_items.append(i)
                    utils_logger.error(f"Элемент {i} не является словарем: {type(item)}")
                    return []

            if invalid_items:
                error_msg = f"Найдены некорректные элементы на позициях: {invalid_items}"
                utils_logger.error(error_msg)
                print(error_msg)
                return []

            utils_logger.info(f"Успешно загружено {len(data)} транзакций из файла: {filepath}")
            return data

    except json.JSONDecodeError as e:
        error_msg = f"Ошибка парсинга JSON в файле {filepath}: {e}"
        utils_logger.error(error_msg)
        print(error_msg)
        return []

    except Exception as e:
        error_msg = f"Неожиданная ошибка при чтении файла {filepath}: {e}"
        utils_logger.exception(error_msg)
        print(error_msg)
        return []
