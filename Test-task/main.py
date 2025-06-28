import argparse
import csv
import sys
import operator
from typing import List, Dict, Optional
from tabulate import tabulate

OPERATORS = {
    '>': operator.gt,
    '<': operator.lt,
    '=': operator.eq
}

AGGREGATIONS = {
    'avg': lambda values: sum(values) / len(values) if values else None,
    'min': min,
    'max': max
}

def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Обработка CSV: фильтрация, агрегация и сортировка.")
    parser.add_argument('--file', required=True, help='Путь к CSV-файлу')
    parser.add_argument('--where', help='Фильтрация, пример: "price>500"')
    parser.add_argument('--aggregate', help='Агрегация, пример: "price=avg"')
    parser.add_argument('--order-by', help='Сортировка, пример: "price=asc"')
    if args is None and len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        raise ValueError("Не переданы аргументы.")
    return parser.parse_args(args)

def read_csv(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

def parse_condition(cond: str):
    for op in OPERATORS:
        if op in cond:
            col, val = cond.split(op, 1)
            return col.strip(), OPERATORS[op], val.strip()
    raise ValueError("Неверное условие фильтрации")

def parse_order(order_str: str):
    if '=' not in order_str:
        raise ValueError("Формат сортировки: column=asc/desc")
    col, direction = order_str.split('=', 1)
    return col.strip(), direction.strip().lower() == 'asc'

def filter_rows(data: List[Dict[str, str]], condition: Optional[str]) -> List[Dict[str, str]]:
    if not condition:
        return data
    col, op, val = parse_condition(condition)
    try:
        val = float(val)
        return [row for row in data if op(float(row[col]), val)]
    except ValueError:
        return [row for row in data if op(row[col], val)]

def aggregate(data: List[Dict[str, str]], instruction: str) -> Dict[str, float]:
    if '=' not in instruction:
        raise ValueError("Формат агрегации: column=agg_func")
    col, func = instruction.split('=', 1)
    func = func.strip().lower()
    if func not in AGGREGATIONS:
        raise ValueError(f"Функция '{func}' не поддерживается")
    try:
        values = [float(row[col.strip()]) for row in data]
    except ValueError:
        raise ValueError(f"Колонка '{col}' должна быть числовой для агрегации")
    return {func: AGGREGATIONS[func](values)}

def sort_data(data: List[Dict[str, str]], order: Optional[str]) -> List[Dict[str, str]]:
    if not order:
        return data
    col, asc = parse_order(order)
    try:
        return sorted(data, key=lambda x: float(x[col]), reverse=not asc)
    except ValueError:
        return sorted(data, key=lambda x: x[col], reverse=not asc)

def main(cli_args=None):
    try:
        args = parse_args(cli_args)
        rows = read_csv(args.file)
        rows = filter_rows(rows, args.where)
        if args.aggregate:
            result = aggregate(rows, args.aggregate)
            print(tabulate([[v] for v in result.values()], headers=result.keys(), tablefmt="grid"))
        else:
            rows = sort_data(rows, args.order_by)
            print(tabulate(rows, headers="keys", tablefmt="grid"))
    except ValueError as ve:
        print(f"Ошибка: {ve}")
        sys.exit(2)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()