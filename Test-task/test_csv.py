import pytest
from csv import DictWriter
from tempfile import NamedTemporaryFile
from main import filter_rows, aggregate, sort_data, parse_condition, parse_order, read_csv

TEST_DATA = [
    {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
    {"name": "galaxy s23 ultra", "brand": "samsung", "price": "1199", "rating": "4.8"},
    {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
    {"name": "poco x5 pro", "brand": "xiaomi", "price": "299", "rating": "4.4"},
]

def write_temp_csv(rows):
    file = NamedTemporaryFile(mode='w+', newline='', delete=False, encoding='utf-8')
    writer = DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
    file.flush()
    return file

def test_filter_numeric():
    filtered = filter_rows(TEST_DATA, "price>500")
    assert len(filtered) == 2
    assert all(float(row["price"]) > 500 for row in filtered)

def test_filter_text():
    filtered = filter_rows(TEST_DATA, "brand=xiaomi")
    assert len(filtered) == 2
    assert all(row["brand"] == "xiaomi" for row in filtered)

def test_aggregate_avg():
    result = aggregate(TEST_DATA, "price=avg")
    assert "avg" in result
    assert round(result["avg"], 2) == 674.0

def test_aggregate_min():
    result = aggregate(TEST_DATA, "rating=min")
    assert result["min"] == 4.4

def test_aggregate_max():
    result = aggregate(TEST_DATA, "price=max")
    assert result["max"] == 1199.0

def test_sort_asc():
    sorted_data = sort_data(TEST_DATA, "price=asc")
    prices = [float(row["price"]) for row in sorted_data]
    assert prices == sorted(prices)

def test_sort_desc():
    sorted_data = sort_data(TEST_DATA, "rating=desc")
    ratings = [float(row["rating"]) for row in sorted_data]
    assert ratings == sorted(ratings, reverse=True)

def test_parse_condition():
    col, op, val = parse_condition("price>100")
    assert col == "price"
    assert op(150, float(val))

def test_parse_order():
    col, asc = parse_order("price=asc")
    assert col == "price"
    assert asc is True

def test_read_csv():
    temp_file = write_temp_csv(TEST_DATA)
    rows = read_csv(temp_file.name)
    assert rows == TEST_DATA
