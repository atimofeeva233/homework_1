import logging
from pathlib import Path


def setup_utils_logger():
    """Настройка логера для модуля utils"""
    # Определяем корневую папку проекта (поднимаемся на два уровня вверх от текущего файла)
    current_file = Path(__file__)  # src/logger_utils.py
    project_root = current_file.parent.parent  # корень проекта

    # Создаем папку logs в корне проекта
    logs_dir = project_root / 'logs'
    logs_dir.mkdir(exist_ok=True)

    logger = logging.getLogger('utils')
    logger.setLevel(logging.DEBUG)

    # Очищаем старые обработчики
    if logger.handlers:
        logger.handlers.clear()

    # Путь к файлу лога
    log_file = logs_dir / 'utils.log'

    file_handler = logging.FileHandler(log_file, 'w', encoding='utf-8')
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger
