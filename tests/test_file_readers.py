from unittest.mock import MagicMock, patch
import pandas as pd
import pytest
from src.file_readers import read_csv_transactions, read_excel_transactions


def test_read_csv_success():
    """Тест без декоратора, с with patch"""
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [{'test': 'data'}]

    with patch('pandas.read_csv', return_value=mock_df) as mock_read_csv:
        result = read_csv_transactions('any_file.csv')

        assert result == [{'test': 'data'}]
        mock_read_csv.assert_called_once_with('any_file.csv')


def test_read_csv_empty_file():
    """Тест чтения пустого CSV файла"""
    mock_df = MagicMock(spec=pd.DataFrame)
    mock_df.to_dict.return_value = []

    with patch('pandas.read_csv', return_value=mock_df):
        result = read_csv_transactions('empty.csv')

        assert result == []
        assert isinstance(result, list)


def test_read_excel_success():
    """Тест успешного чтения Excel файла"""
    # Создаем mock DataFrame
    mock_df = MagicMock(spec=pd.DataFrame)

    # Тестовые данные
    test_data = [
        {'date': '2023-01-01', 'amount': 150.50, 'description': 'Groceries'},
        {'date': '2023-01-03', 'amount': 75.20, 'description': 'Coffee'},
        {'date': '2023-01-04', 'amount': 1000.00, 'description': 'Salary'}
    ]
    mock_df.to_dict.return_value = test_data

    # Патчим pandas.read_excel
    with patch('pandas.read_excel', return_value=mock_df) as mock_read_excel:
        # Вызываем функцию
        result = read_excel_transactions('transactions.xlsx')

        # Проверки
        assert result == test_data
        assert len(result) == 3
        assert result[2]['amount'] == 1000.00
        assert 'description' in result[0]

        mock_read_excel.assert_called_once_with('transactions.xlsx')
        mock_df.to_dict.assert_called_once_with('records')


def test_read_excel_empty_file():
    """Тест чтения пустого Excel файла"""
    mock_df = MagicMock(spec=pd.DataFrame)
    mock_df.to_dict.return_value = []

    with patch('pandas.read_excel', return_value=mock_df):
        result = read_excel_transactions('empty.xlsx')

        assert result == []
        assert isinstance(result, list)


def test_read_excel_file_not_found():
    """Тест обработки ошибки при отсутствии Excel файла"""
    with patch('pandas.read_excel', side_effect=FileNotFoundError("Excel file not found")):
        with pytest.raises(FileNotFoundError):
            read_excel_transactions('nonexistent.xlsx')


def test_both_functions_return_same_structure():
    """Тест, что обе функции возвращают данные одинаковой структуры"""
    # Тестовые данные
    test_data = [
        {'date': '2023-01-01', 'amount': 100, 'category': 'food'}
    ]

    # Создаем mock DataFrame
    mock_df = MagicMock(spec=pd.DataFrame)
    mock_df.to_dict.return_value = test_data

    # Тестируем обе функции
    with patch('pandas.read_csv', return_value=mock_df):
        with patch('pandas.read_excel', return_value=mock_df):
            csv_result = read_csv_transactions('test.csv')
            excel_result = read_excel_transactions('test.xlsx')

            # Проверяем, что структура данных одинаковая
            assert csv_result == excel_result
            assert isinstance(csv_result, list)
            assert isinstance(excel_result, list)
            assert all(isinstance(item, dict) for item in csv_result)
