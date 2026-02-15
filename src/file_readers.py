import pandas as pd


def read_csv_transactions(file_path):
    """
        Читает финансовые транзакции из CSV файла и возвращает их в виде списка словарей.

        Параметры:
            file_path (str): Путь к CSV файлу.

        Возвращает:
            list[dict]: Список словарей, где каждый словарь представляет одну транзакцию.
                        Ключи словаря соответствуют названиям колонок в CSV файле.
        """
    df = pd.read_csv(file_path)
    transactions = df.to_dict('records')
    return transactions


def read_excel_transactions(file_path):
    """
        Читает финансовые транзакции из Excel файла и возвращает их в виде списка словарей.

        Параметры:
            file_path (str): Путь к Excel файлу.

        Возвращает:
            list[dict]: Список словарей, где каждый словарь представляет одну транзакцию.
                        Ключи словаря соответствуют названиям колонок в Excel файле.
        """
    df = pd.read_excel(file_path)
    transactions = df.to_dict('records')
    return transactions
