from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    '''
    Декоратор для логирования выполнения функций.

    :param filename: Путь к файлу для записи логов. Если None - вывод в консоль.

    :return: Декоратор для функции.
    '''
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                result = func(*args, **kwargs)

                # Формирование сообщения об успешном выполнении
                success_msg = f'{func.__name__} ok'

                # Записываем или выводим сообщение
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(success_msg + '\n')
                else:
                    print(success_msg)

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_msg = f'{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}'

                # Записываем или выводим сообщение
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(error_msg + '\n')
                else:
                    print(error_msg)

                raise

        return wrapper

    return decorator
