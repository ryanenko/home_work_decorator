import requests
import os
from datetime import datetime

def logger(param):    
    """Параметризированный декоратор """
    def _logger(old_function):

        """Декоратор для создания файла  и записи в него даты и времени вызова основной функции, ее имени, агрументов и результата"""
        def new_function(*args, **kwargs):
            date_time = datetime.now()
            function_time = date_time.strftime('%Y-%m-%d время %H-%M-%S')
            function_name = old_function.__name__
            function_result = old_function(*args, **kwargs)
            with open(param, 'a', encoding='utf-8') as file:
                file.write(f'\nДата вызова функции: {function_time}\n'
                    f'Имя функции: {function_name}\n'
                    f'Аргументы функции: {args, kwargs}\n'
                    f'Возвращаемое значение функции: {function_result}\n'
                    f'{"*"*50}\n')
            return function_result
        return new_function
    return _logger

def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(param=path)
        def hello_world():
            return 'Hello World'

        @logger(param=path)
        def summator(a, b=0):
            return a + b

        @logger(param=path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path, 'rt', encoding='utf-8') as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()