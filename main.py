import os

from src.file_readers import read_csv_transactions, read_excel_transactions
from src.logger_utils import setup_utils_logger
from src.processing import sort_by_date
from src.search import process_bank_search
from src.utils import load_trans_from_json

logger = setup_utils_logger()

# Зададим постоянные величины
VALID_STATUSES = {'EXECUTED', 'CANCELED', 'PENDING'}
CURRENCY_CODES = {'rub': 'руб.', 'usd': 'USD', 'eur': 'EUR'}
FILE_PATHS = {
    "1": "data/operations.json",
    "2": "data/operations.csv",
    "3": "data/operations.xlsx"
}


def get_file_choice() -> str:
    '''Получает от пользователя выбор файла для загрузки'''
    print('\nПрограмма: Привет! Добро пожаловать в программу работы с банковскими транзакциями.')
    print('Выберите необходимый пункт меню:')
    print('1. Получить информацию о транзакциях из JSON-файла')
    print('2. Получить информацию о транзакциях из CSV-файла')
    print('3. Получить информацию о транзакциях из XLSX-файла')

    while True:
        choice = input('Пользователь: ').strip()
        if choice in ['1', '2', '3']:
            file_types = {'1': 'JSON', '2': 'CSV', '3': 'XLSX'}
            print(f'Программа: Для обработки выбран {file_types[choice]}-файл.')
            return choice
        print('Неверный ввод. Пожалуйста, введите 1, 2 или 3.')


def load_transactions(file_choice: str, file_path: str) -> list:
    """
    Загружает транзакции из файла в зависимости от выбранного формата
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            logger.warning(f"Файл {file_path} не найден")
            print(f"\nПрограмма: Файл {file_path} не найден. Будут использованы тестовые данные.")
            return get_test_data()

        if file_choice == "1":
            return load_trans_from_json(file_path)
        elif file_choice == "2":
            # Используем функцию из file_readers
            return read_csv_transactions(file_path)
        elif file_choice == "3":
            # Используем функцию из file_readers
            return read_excel_transactions(file_path)
    except ImportError as e:
        logger.error(f"Не удалось импортировать модуль для чтения: {e}")
        print(f"\nПрограмма: Библиотека для чтения {file_choice} не установлена.")
        return get_test_data()
    except Exception as e:
        logger.error(f"Ошибка загрузки: {e}")
        return get_test_data()
    return []


def get_valid_status() -> str:
    '''Запрашивает у пользователя статус и проверяет его корректность'''
    print('\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.')
    print('Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING')

    while True:
        status = input('Пользователь: ').strip().upper()
        if status in VALID_STATUSES:
            print(f'\nПрограмма: Операции отфильтрованы по статусу \"{status}\"')
            return status
        print(f'\nПрограмма: Статус операции "{status}" недоступен.')


def get_yes_no(prompt: str) -> bool:
    '''Запрашивает у пользователя ответ Да/Нет'''
    while True:
        answer = input(f'\nПрограмма: {prompt} Да/Нет\nПользователь: ').strip().lower()
        if answer in ['да', 'нет', 'yes', 'no', 'y', 'n']:
            return answer in ['да', 'yes', 'y']
        print('\nПрограмма: Пожалуйста, введите "Да" или "Нет"')


def get_sort_order() -> str:
    '''Запрашивает порядок сортировки'''
    while True:
        order = input('\nПрограмма: Отсортировать по возсрастанию или по убыванию?\nПользователь: ').strip().lower()
        if order in ['по возрастанию', 'по убыванию', 'возрастанию', 'убыванию', 'asc', 'desc']:
            return 'убыванию' if order in ['по убыванию', 'убыванию', 'desc'] else 'возрастанию'
        print('\nПрограмма: Пожалуйста, введите "по возрастанию" или "по убыванию"')


def format_transaction(transaction: dict) -> str:
    """Форматирует транзакцию для вывода"""
    date = transaction.get("date", "")
    if date:
        date = date[:10].replace("-", ".")
        # Форматирование даты из ISO в DD.MM.YYYY
        if len(date) == 10:
            date_parts = date.split(".")
            if len(date_parts) == 3:
                date = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
    else:
        date = ""

    description = transaction.get("description", "")

    # Просто берем строки как есть
    from_str = transaction.get("from", "")
    to_str = transaction.get("to", "")

    # Получаем сумму и валюту
    amount = transaction.get("operationAmount", {}).get("amount", transaction.get("amount", ""))
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("code", transaction.get("currency", ""))

    # Определяем символ валюты
    currency_symbol = CURRENCY_CODES.get(currency.lower() if currency else "", currency)

    # Формируем вывод
    result = f"\n{date} {description}\n"

    if from_str and to_str:
        result += f"{from_str} -> {to_str}\n"
    elif to_str:
        result += f"{to_str}\n"

    if amount:
        result += f"Сумма: {amount} {currency_symbol}\n"

    return result


def get_test_data() -> list:
    """Возвращает тестовые данные для демонстрации"""
    logger.info("Используются тестовые данные")
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-12T20:41:47.882230",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560"
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "EUR", "code": "EUR"}
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963004202"
        },
        {
            "id": 587085106,
            "state": "CANCELED",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {
                "amount": "48223.05",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431"
        }
    ]


def main():
    """Основная логика программы"""
    logger.info("Запуск программы main")

    try:
        # Шаг 1: Выбор файла
        file_choice = get_file_choice()
        file_path = FILE_PATHS[file_choice]
        logger.info(f"Выбран файл: {file_path}")

        # Шаг 2: Загрузка транзакций
        transactions = load_transactions(file_choice, file_path)

        # Если файл не найден или ошибка загрузки, load_transactions вернет тестовые данные
        if not transactions:
            print("\nПрограмма: Не удалось загрузить транзакции.")
            logger.error("Не удалось загрузить транзакции")
            return

        # Шаг 3: Сортировка по дате
        if get_yes_no("Отсортировать операции по дате?"):
            order = get_sort_order()
            reverse = order == "убыванию"
            filtered_by_status = sort_by_date(filtered_by_status, reverse)
            logger.info(f"Транзакции отсортированы по дате ({order})")

        # Шаг 4: Фильтрация по рублевым транзакциям
        if get_yes_no("Выводить только рублевые транзакции?"):
            rub_transactions = []
            for t in filtered_by_status:
                currency = t.get("operationAmount", {}).get("currency", {}).get("code", "")
                if currency.upper() == "RUB":
                    rub_transactions.append(t)
            filtered_by_status = rub_transactions
            logger.info(f"После фильтрации по RUB: {len(filtered_by_status)} транзакций")

        # Шаг 5: Фильтрация по слову в описании
        if get_yes_no("Отфильтровать список транзакций по определенному слову в описании?"):
            search_word = input("\nПрограмма: Введите слово для поиска:\nПользователь: ").strip()
            filtered_by_status = process_bank_search(filtered_by_status, search_word)
            logger.info(f"После фильтрации по слову '{search_word}': {len(filtered_by_status)} транзакций")

        # Шаг 6: Вывод результатов
        print("\nПрограмма: Распечатываю итоговый список транзакций...")

        if not filtered_by_status:
            print("\nПрограмма: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
            logger.info("Не найдено транзакций после всех фильтров")
            return

        print(f"\nПрограмма: \nВсего банковских операций в выборке: {len(filtered_by_status)}")

        for transaction in filtered_by_status:
            print(format_transaction(transaction))

        logger.info(f"Выведено {len(filtered_by_status)} транзакций")

    except KeyboardInterrupt:
        print("\n\nПрограмма: Работа программы прервана пользователем.")
        logger.info("Программа прервана пользователем")
    except Exception as e:
        print(f"\nПрограмма: Произошла ошибка: {e}")
        logger.exception(f"Ошибка в работе программы: {e}")


if __name__ == "__main__":
    main()
