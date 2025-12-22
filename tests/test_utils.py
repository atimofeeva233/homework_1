import pytest
import json
import os
from unittest.mock import mock_open, patch, MagicMock
from src.utils import load_trans_from_json


def test_load_transactions_from_json_success():
    """Тест успешной загрузки JSON файла."""
    # Мокаем данные
    mock_data = [
        {"id": 1, "state": "EXECUTED", "amount": "100.00"},
        {"id": 2, "state": "CANCELED", "amount": "200.00"}
    ]
    mock_json_content = json.dumps(mock_data)

    # Мокаем все внешние зависимости
    with patch('builtins.open', mock_open(read_data=mock_json_content)) as mock_file, \
            patch('os.path.exists', return_value=True), \
            patch('os.path.isfile', return_value=True), \
            patch('os.path.getsize', return_value=100):
        result = load_trans_from_json('test.json')

        assert result == mock_data
        mock_file.assert_called_once_with('test.json', 'r', encoding='utf-8')


def test_load_trans_from_json_file_not_exists():
    """Тест случая, когда файл не существует"""
    with patch('os.path.exists', return_value=False), \
            patch('builtins.print') as mock_print:
        result = load_trans_from_json('nonexistent.json')

        assert result == []
        mock_print.assert_called_once_with('Файл не найден: nonexistent.json')


def test_load_trans_from_json_path_is_directory():
    """Тест случая, когда путь указывает на директорию"""
    with patch('os.path.exists', return_value=True), \
            patch('os.path.isfile', return_value=False), \
            patch('builtins.print') as mock_print:
        result = load_trans_from_json('/some/directory')

        assert result == []
        mock_print.assert_called_once_with('Указанный путь не является файлом: /some/directory')


def test_load_trans_from_json_empty_file():
    """Тест случая с пустым файлом"""
    with patch('os.path.exists', return_value=True), \
            patch('os.path.isfile', return_value=True), \
            patch('os.path.getsize', return_value=0), \
            patch('builtins.print') as mock_print:
        result = load_trans_from_json('empty.json')

        assert result == []
        mock_print.assert_called_once_with('Файл пустой: empty.json')


def test_load_trans_from_json_invalid_json():
    """Тест случая с некорректным JSON"""
    with patch('builtins.open', mock_open(read_data='invalid json')), \
            patch('os.path.exists', return_value=True), \
            patch('os.path.isfile', return_value=True), \
            patch('os.path.getsize', return_value=100), \
            patch('builtins.print') as mock_print:
        result = load_trans_from_json('invalid.json')

        assert result == []
        mock_print.assert_called_once()
