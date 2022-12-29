import json
import csv
import os
import calendar
from pprint import pprint

import date

MONTH_NAMES = tuple(m.upper() for m in calendar.month_name)

def _xor(p: bool, q: bool) -> bool:
    return (not p and q) or (p and not q)

def _sort(files: list) -> list:
    unsorted_files = [[f, _get_date(f)] for f in files]
    return [f[0] for f in sorted(unsorted_files, key=lambda date: date[1], reverse=True)]

def _get_date(file_name: str) -> tuple:
    year_month = file_name.split(os.path.sep)[-1][:-5]
    year, month = year_month.split('_')
    return int(year), MONTH_NAMES.index(month)

def generate_csv(source: str, destination: str) -> None:
    valid_path = [
        os.path.join('Takeout', '위치 기록', 'Semantic Location History'),
        os.path.join('Takeout', 'Location History', 'Semantic Location History')
    ]

    json_files = source.getnames()

    unsorted_files = [f for f in json_files if _xor(valid_path[0] in f, valid_path[1] in f)]
    sorted_files = _sort(unsorted_files)
