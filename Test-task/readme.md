# CSV Query Tool

Инструмент командной строки на Python для фильтрации, агрегации и сортировки данных из CSV-файла.

## Возможности

- Загрузка CSV с произвольными колонками.
- Фильтрация (`--where`) по одной колонке с операторами `>`, `<`, `=`.
- Агрегация (`--aggregate`) с функциями `avg`, `min`, `max` для числовых данных.
- Сортировка (`--order-by`) по любой колонке в `asc` или `desc` порядке.
- Красивый вывод в консоли через [tabulate](https://pypi.org/project/tabulate/).

## Пример CSV

```csv
name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4
```

## Установка

```bash
pip install tabulate
```

## Использование

```bash
python main.py --file products.csv
```

### Фильтрация

```bash
python main.py --file products.csv --where "price>500"
```

### Агрегация

```bash
python main.py --file products.csv --aggregate "price=avg"
```

### Сортировка

```bash
python main.py --file products.csv --order-by "rating=desc"
```

Можно комбинировать:

```bash
python main.py --file products.csv --where "brand=xiaomi" --order-by "price=asc"
```

## Тестирование

Для запуска тестов требуется `pytest`:

```bash
pytest
```

### Покрытие тестами

Скрипт покрыт модульными тестами более чем на 80%:
- фильтрация по числам и строкам
- агрегации: avg, min, max
- сортировка по возрастанию и убыванию
- разбор аргументов фильтрации и сортировки
- чтение CSV-файла

## Структура

- `main.py` — основной скрипт
- `products.csv` — пример входного файла
- `README.md` — документация

## Ограничения

- Только одна фильтрация и одна агрегация за запуск
- Только числовые колонки поддерживаются в агрегации
<<<<<<< HEAD
- Сложные фильтры (`AND`, `OR`, `!=`) не поддерживаются
=======
- Сложные фильтры (`AND`, `OR`, `!=`) не поддерживаются
>>>>>>> 0c28ded12c726881e8f816f9fbbd491273d45d55
