# Импорт необходимых модулей
import argparse  # Для обработки аргументов командной строки
import csv  # Для работы c CSV файлами
from tabulate import tabulate  # Для красивого вывода таблиц
from typing import List, Dict, Union, Optional, Tuple  # Аннотации типов


class CSVProcessor:
    """Основной класс для обработки CSV файлов c поддержкой фильтрации, сортировки и агрегации."""
    
    def __init__(self, filename: str):
        """Инициализация процессора CSV файлов.
        
        Args:
            filename (str): Путь к CSV файлу для обработки
        """
        self.filename = filename  # Сохраняем путь к файлу
        self.data = self._read_csv()  # Загружаем данные из файла
        
    def _read_csv(self) -> List[Dict[str, Union[str, float]]]:
        """Чтение CSV файла и преобразование данных.
        
        Returns:
            List[Dict[str, Union[str, float]]: Список строк, где каждая строка - словарь значений
        """
        with open(self.filename, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)  # Читаем как словари
            return [self._convert_numeric_values(row) for row in reader]  # Преобразуем числа
    
    def _convert_numeric_values(self, row: Dict[str, str]) -> Dict[str, Union[str, float]]:
        """Автоматическое преобразование числовых значений в float.
        
        Args:
            row (Dict[str, str]): Строка данных из CSV
            
        Returns:
            Dict[str, Union[str, float]]: Строка c преобразованными числами
        """
        processed_row = {}
        for key, value in row.items():
            try:
                processed_row[key] = float(value)  # Пробуем преобразовать в число
            except ValueError:
                processed_row[key] = value  # Оставляем строку, если не число
        return processed_row
    
    def filter_data(self, condition: str) -> List[Dict[str, Union[str, float]]]:
        """Фильтрация данных по условию.
        
        Args:
            condition (str): Условие в формате "колонка=значение", "колонка>значение" или "колонка<значение"
            
        Returns:
            List[Dict[str, Union[str, float]]]: Отфильтрованные данные
        """
        # Разбираем условие на составляющие
        column, operator, value = self._parse_condition(condition)
        
        filtered_data = []
        for row in self.data:
            row_value = row.get(column)
            if row_value is None:  # Пропускаем если колонка отсутствует
                continue
                
            # Применяем оператор фильтрации    
            if operator == '=' and row_value == value:
                filtered_data.append(row)
            elif operator == '>' and isinstance(row_value, (int, float)) and row_value > value:
                filtered_data.append(row)
            elif operator == '<' and isinstance(row_value, (int, float)) and row_value < value:
                filtered_data.append(row)
        
        return filtered_data
    
    def _parse_condition(self, condition: str) -> Tuple[str, str, Union[str, float]]:
        """Разбор строки условия на компоненты.
        
        Args:
            condition (str): Строка условия
            
        Returns:
            Tuple[str, str, Union[str, float]]: (колонка, оператор, значение)
            
        Raises:
            ValueError: Если формат условия некорректен
        """
        operators = ['>', '<', '=']  # Поддерживаемые операторы
        for op in operators:
            if op in condition:
                parts = condition.split(op)
                if len(parts) == 2:  # Проверяем что условие разбилось на 2 части
                    column = parts[0].strip()  # Название колонки
                    value = parts[1].strip()  # Значение для сравнения
                    
                    # Пробуем преобразовать значение в число
                    try:
                        value = float(value)
                    except ValueError:
                        pass  # Оставляем строкой если не число
                        
                    return (column, op, value)
        
        raise ValueError(f"Некорректный формат условия: {condition}")
    
    def aggregate(self, aggregation: str, data: Optional[List[Dict[str, Union[str, float]]]] = None) -> Dict[str, float]:
        """Агрегация данных по указанной колонке.
        
        Args:
            aggregation (str): Условие агрегации в формате "колонка=операция"
            data (Optional[List[Dict]]): Данные для агрегации (если None, используются все данные)
            
        Returns:
            Dict[str, float]: Результат агрегации c ключом-названием операции
            
        Raises:
            ValueError: Если операция агрегации неизвестна
        """
        # Разбиваем условие агрегации
        column, operation = aggregation.split('=')
        column, operation = column.strip(), operation.strip().lower()
        
        # Собираем все числовые значения из указанной колонки
        values = [row[column] for row in (data if data else self.data) 
                 if isinstance(row.get(column), (int, float))]
        
        if not values:  # Если нет значений для агрегации
            return {operation: 0.0}
        
        # Доступные операции агрегации
        operations = {
            'avg': lambda: sum(values) / len(values),  # Среднее значение
            'min': lambda: min(values),  # Минимальное значение
            'max': lambda: max(values),  # Максимальное значение
        }
        
        if operation not in operations:
            raise ValueError(f"Неизвестная операция агрегации: {operation}")
        
        return {operation: operations[operation]()}  # Выполняем и возвращаем результат
    
    def sort_data(self, order_by: str, data: Optional[List[Dict[str, Union[str, float]]]] = None) -> List[Dict[str, Union[str, float]]]:
        """Сортировка данных по указанной колонке.
        
        Args:
            order_by (str): Условие сортировки в формате "колонка=направление"
            data (Optional[List[Dict]]): Данные для сортировки (если None, используются все данные)
            
        Returns:
            List[Dict]: Отсортированные данные
            
        Raises:
            ValueError: Если направление сортировки не 'asc' или 'desc'
        """
        # Разбираем параметры сортировки
        column, direction = order_by.split('=')
        column, direction = column.strip(), direction.strip().lower()
        
        if direction not in ('asc', 'desc'):
            raise ValueError("Направление сортировки должно быть 'asc' или 'desc'")
        
        # Используем переданные данные или все данные
        data_to_sort = data if data else self.data.copy()
        
        # Определяем, содержит ли колонка числовые значения
        is_numeric = all(isinstance(row.get(column), (int, float)) 
                        for row in data_to_sort 
                        if column in row and row[column] is not None)
        
        def sort_key(row):
            """Функция для определения порядка сортировки."""
            value = row.get(column)
            # Для числовых и строковых значений разная логика сортировки
            return (value is None, value) if not is_numeric else (value is None, float(value))
        
        # Сортируем с учетом направления
        return sorted(data_to_sort, key=sort_key, reverse=(direction == 'desc'))


def main():
    """Главная функция для обработки аргументов командной строки."""
    # Настройка парсера аргументов
    parser = argparse.ArgumentParser(description='Обработчик CSV файлов c фильтрацией, сортировкой и агрегацией')
    parser.add_argument('--file', required=True, help='Путь к CSV файлу')
    parser.add_argument('--where', help='Условие фильтрации (например: "цена>500")')
    parser.add_argument('--aggregate', help='Условие агрегации (например: "рейтинг=avg")')
    parser.add_argument('--order-by', help='Условие сортировки (например: "название=asc")')
    
    args = parser.parse_args()  # Парсим аргументы
    
    # Инициализируем процессор
    processor = CSVProcessor(args.file)
    data = processor.data  # Исходные данные
    
    # Применяем фильтрацию если указана
    if args.where:
        data = processor.filter_data(args.where)
    
    # Применяем сортировку если указана
    if args.order_by:
        data = processor.sort_data(args.order_by, data)
    
    # Применяем агрегацию если указана
    if args.aggregate:
        result = processor.aggregate(args.aggregate, data)
        print(tabulate([result], headers="keys", tablefmt="grid"))  # Красивый вывод
    else:
        # Выводим данные если нет агрегации
        if data:
            print(tabulate(data, headers="keys", tablefmt="grid"))
        else:
            print("Нет данных, соответствующих критериям")


if __name__ == '__main__':
    # Точка входа при запуске скрипта напрямую
    main()