# Проект Bank_Card
## Описание:
Проект Bank_Card - это комплексное решение для обработки и анализа банковских транзакций клиентов. 
Система предоставляет инструменты для маскирования конфиденциальных данных, фильтрации, сортировки и 
генерации отчетов по транзакциям.

## Основные функции:

### 1. **Обработка транзакций**
- Маскирование номеров карт (формат: XXXX XX** **** XXXX)
- Маскирование номеров счетов (формат: **XXXX)
- Безопасное отображение финансовых данных

### 2. **Фильтрация и поиск**
- Фильтрация транзакций по статусу (EXECUTED, CANCELED, PENDING)
- Фильтрация по описанию с использованием регулярных выражений
- Поиск транзакций по ключевым словам
- Подсчет транзакций по категориям

### 3. **Сортировка**
- Сортировка транзакций по дате (возрастание/убывание)
- Стабильная сортировка с сохранением порядка при одинаковых датах

### 4. **Чтение данных из разных форматов**
- Поддержка JSON-файлов
- Поддержка CSV-файлов (с использованием pandas)
- Поддержка Excel-файлов (XLSX)
- Единый формат данных для всех источников

### 5. **Логирование**
- Автоматическое логирование всех операций
- Отдельные лог-файлы для каждого модуля (`logs/`)
- Детальная запись успешных и ошибочных операций
- Формат: timestamp - модуль - уровень - сообщение

## Установка:
1. Клонируйте репозиторий:
```
git clone https://github.com/username/homework_1.git
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
## Использование:
```
python main.py
```
Программа предложит:

Выбор формата файла (JSON/CSV/XLSX)

Фильтрацию по статусу транзакций

Сортировку по дате

Фильтрацию по рублевым операциям

Поиск по ключевым словам в описании

### Основные функции:

#### Маскирование данных:
```python
from src.masks import get_mask_card_number, get_mask_account

# Маскирование номера карты
masked_card = get_mask_card_number("1234567890123456")  # "1234 56** **** 3456"

# Маскирование номера счета
masked_account = get_mask_account("12345678901234567890")  # "**7890"

# Фильтрация транзакций:

from src.generators import filter_by_currency

# Фильтрация транзакций по валюте USD
usd_transactions = list(filter_by_currency(transactions, "USD"))

# Сортировка транзакций:
from src.processing import sort_by_date

# Сортировка транзакций по дате (по убыванию)
sorted_transactions = sort_by_date(transactions, reverse=True)

# Генераторы:
from src.generators import transaction_descriptions, card_number_generator

# Получение описаний транзакций
descriptions = list(transaction_descriptions(transactions))

# Генерация номеров карт
card_numbers = list(card_number_generator(1, 10))

# Декораторы для логирования
from src.decorators import log, timer, retry

# Логирование в консоль
@log()
def process_payment(amount, currency):
    """Обработка платежа"""
    return f"Processed {amount} {currency}"

# Логирование в файл
@log(filename="payments.log")
@retry(max_attempts=3)
def risky_operation(data):
    """Операция с повторными попытками"""
    if not validate(data):
        raise ValueError("Invalid data")
    return process(data)

#### Чтение данных из файлов:
```python
from src.file_readers import read_csv_transactions, read_excel_transactions

# Чтение транзакций из CSV файла
csv_transactions = read_csv_transactions("data/transactions.csv")

# Чтение транзакций из Excel файла
excel_transactions = read_excel_transactions("data/transactions_excel.xlsx")

# Обе функции возвращают список словарей с транзакциями
for transaction in csv_transactions:
    print(f"{transaction['date']}: {transaction['amount']} {transaction['currency']}")
```
## Тестирование:
### Запуск тестов:
```
bash
# Запуск всех тестов
pytest

# Запуск тестов с детальным выводом
pytest -v

# Запуск конкретного тестового файла
pytest tests/test_masks.py

# Запуск тестов с покрытием кода
pytest --cov=src tests/
```
### Структура тестов:
#### Тесты для маскирования данных (tests/test_masks.py):
Тестирование функции get_mask_card_number\
Тестирование функции get_mask_account\
Проверка обработки некорректных данных\
Тесты граничных случаев

#### Тесты для обработки транзакций (tests/test_processing.py):
Тестирование функции sort_by_date\
Проверка стабильной сортировки (сохранение порядка при одинаковых датах)\
Тесты с нестандартными форматами дат\
Тесты с пустыми и некорректными данными

#### Тесты для генераторов (tests/test_generators.py):
Тестирование функции filter_by_currency\
Тестирование генератора transaction_descriptions\
Тестирование генератора card_number_generator\
Проверка поведения итераторов\
Тесты граничных значений

#### Тесты для декораторов (tests/test_decorators.py)
Тестирование декоратора log
Проверка вывода в консоль и файл
Тесты обработки ошибок
Проверка формата логов

#### Тесты для чтения файлов (tests/test_file_readers.py):
Тестирование функции read_csv_transactions\
Тестирование функции read_excel_transactions\
Проверка обработки пустых файлов\
Тестирование обработки ошибок при отсутствии файла\
Проверка структуры возвращаемых данных\
Использование Mock и patch для изоляции тестов

## Покрытие тестами:
```
# Запуск с проверкой покрытия
pytest --cov=src tests/

# Создание HTML-отчета о покрытии
pytest --cov=src --cov-report=html tests/

# Открыть отчет в браузере (Windows)
start htmlcov/index.html

# Открыть отчет (MacOS/Linux)
open htmlcov/index.html
```
### Текущее покрытие:
Проект имеет высокое покрытие тестами. Отчет о покрытии можно посмотреть в папке `htmlcov/`.

### Генерация отчета о покрытии:
```bash
# Генерация отчета о покрытии в формате HTML
pytest --cov=src --cov-report=html tests/

# После выполнения команды откройте файл:
open htmlcov/index.html
# Или в Windows:
start htmlcov/index.html
```

## Документация:

Для получения дополнительной информации обратитесь к [документации](docs/README.md).

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE).