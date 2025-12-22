import os
import tempfile
import pytest
from src.decorators import log


def test_log_to_console(capsys):
    @log()
    def add(a: int, b: int) -> int:
        return a + b
    result = add(2, 3)
    assert result == 5

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert captured.out.strip() == 'add ok'


def test_log_to_console_with_kwargs(capsys):
    @log()
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    result = greet("Anna", greeting="Hi")

    # Проверяем результат
    assert result == "Hi, Anna!"

    # Проверяем вывод
    captured = capsys.readouterr()
    assert captured.out.strip() == "greet ok"


def test_log_to_console_error(capsys):
    @log()
    def divide(a: int, b: int) -> float:
        if b == 0:
            raise ZeroDivisionError('division by zero')
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

        # Проверяем вывод
        captured = capsys.readouterr()
        assert "divide error: ZeroDivisionError. Inputs: (10, 0), {}" in captured.out


def test_log_to_file_success():
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
        tmp_file = tmp.name
    try:
        @log(filename=tmp_file)
        def multiply(a: int, b: int) -> int:
            return a * b
        result = multiply(4, 5)

        # Проверяем результат
        assert result == 20

        # Проверяем содержимое файла
        with open(tmp_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        assert content == "multiply ok"
    finally:

        # Удаляем временный файл
        os.unlink(tmp_file)


def test_log_to_file_error():

    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
        tmp_file = tmp.name

    try:
        @log(filename=tmp_file)
        def dangerous_operation(x: int) -> int:
            if x > 100:
                raise RuntimeError("Value too large")
            return x

        # Проверяем успешное выполнение
        result = dangerous_operation(50)
        assert result == 50

        # Проверяем ошибку
        with pytest.raises(RuntimeError):
            dangerous_operation(150)

        # Проверяем содержимое файла
        with open(tmp_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        assert len(lines) == 2
        assert lines[0].strip() == "dangerous_operation ok"
        assert "dangerous_operation error: RuntimeError. Inputs: (150,), {}" in lines[1]

    finally:
        os.unlink(tmp_file)


def test_log_to_file_multiple_calls():

    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
        tmp_file = tmp.name

    try:
        @log(filename=tmp_file)
        def counter() -> int:
            if not hasattr(counter, 'count'):
                counter.count = 0
            counter.count += 1
            return counter.count

        # Вызываем несколько раз
        results = [counter() for _ in range(3)]

        assert results == [1, 2, 3]

        # Проверяем содержимое файла
        with open(tmp_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]

        assert len(lines) == 3
        assert all(line == "counter ok" for line in lines)

    finally:
        os.unlink(tmp_file)


def test_log_preserves_function_metadata():

    @log()
    def original_function(x: int, y: int) -> int:
        """Это оригинальная функция"""
        return x + y

    # Проверяем сохранение имени
    assert original_function.__name__ == "original_function"

    # Проверяем сохранение документации
    assert original_function.__doc__ == "Это оригинальная функция"


def test_log_with_empty_args():

    @log()
    def get_answer() -> int:
        return 42

    result = get_answer()
    assert result == 42


def test_log_with_complex_args():

    @log()
    def process_data(data: list, default: dict ) -> list:
        if default is None:
            default = {}
        return data + list(default.values())

    result = process_data([1, 2], default={'a': 3, 'b': 4})
    assert result == [1, 2, 3, 4]
