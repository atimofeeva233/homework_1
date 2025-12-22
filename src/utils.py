import json
import os
from typing import Any, Dict, List


def load_trans_from_json(filepath: str) -> List[Dict[str, Any]]:
    '''
    Функция загружает транзакции  из JSON-файла

    :param filepath: путь до JSON-файла

    :return: List[Dict[str, Any]]: Список словарей с данными о транзакциях.
    Возвращает пустой список в случае ошибок.
    '''
    try:
        # Проверяем существование файла
        if not os.path.exists(filepath):
            print(f'Файл не найден: {filepath}')
            return []

        # Проверяем, что это файл, а не директория
        if not os.path.isfile(filepath):
            print(f'Указанный путь не является файлом: {filepath}')
            return []

        # Проверяем размер файла
        if os.path.getsize(filepath) == 0:
            print(f"Файл пустой: {filepath}")
            return []

        # Читаем файл
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read().strip()

            data = json.loads(content)

            # Проверяем, что данные - это список
            if not isinstance(data, list):
                print(f"JSON не содержит список на верхнем уровне: {filepath}")
                return []

            # Проверяем, что все элементы списка - словари
            for i, item in enumerate(data):
                if not isinstance(item, dict):
                    print(f"Элемент {i} не является словарем: {type(item)}")
                    return []

            return data

    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON в файле {filepath}: {e}")
        return []

    except Exception as e:
        print(f"Неожиданная ошибка при чтении файла {filepath}: {e}")
        return []
