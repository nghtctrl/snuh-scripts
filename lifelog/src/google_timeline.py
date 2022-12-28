import json
import csv
import os
import calendar

import date

month_names = [m.upper() for m in calendar.month_name]

def _xor(p: bool, q: bool) -> bool:
    return (not p and q) or (p and not q)

def _date_from_filename(filename: str) -> tuple:
    # Extract "YEAR_MONTH" from the Semantic Location History JSON filename
    temp = filename.split(os.path.sep)[-1][:-5]

    # Extract the year and month from the filename
    year, month = temp.split('_')

    # Return the numeric version of each values
    return int(year), month_names.index(month)

def generate_csv(source: str, destination: str) -> None:
    valid_path = [
        os.path.join('Takeout', '위치 기록', 'Semantic Location History'),
        os.path.join('Takeout', 'Location History', 'Semantic Location History')
    ]
    json_files = source.getnames()
    unsorted_location_history_files = [f for f in json_files if _xor(valid_path[0] in f, valid_path[1] in f)]
    pprint(unsorted_location_history_files)

    if len(unsorted_location_history_files) > 0:
        sorted_location_history_files = sorted(unsorted_location_history_files, key=_get_year_month)
        pprint(sorted_location_history_files)

import unittest
import random

class TestGoogleTimeline(unittest.TestCase):
    def test_xor(self):
        self.assertEqual(_xor(True, True), False)
        self.assertEqual(_xor(True, False), True)
        self.assertEqual(_xor(False, True), True)
        self.assertEqual(_xor(False, False), False)

    def test_date_from_filename(self):
        template = os.path.join('Takeout', '{}', 'Semantic Location History', '{}', '{}_{}.json')

        # User defined case
        test_case_input = [
            template.format('위치 기록', '2021', '2021', 'SEPTEMBER'),
            template.format('위치 기록', '2021', '2021', 'OCTOBER'),
            template.format('위치 기록', '2021', '2021', 'NOVEMBER'),
            template.format('위치 기록', '2021', '2021', 'DECEMBER'),
            template.format('위치 기록', '2022', '2022', 'JANUARY'),
            template.format('위치 기록', '2022', '2022', 'FEBRUARY')
        ]

        test_case_output = [
            (2021, 9),
            (2021, 10),
            (2021, 11),
            (2021, 12),
            (2022, 1),
            (2022, 2),
        ]

        for i in range(len(test_case_input)):
            self.assertEqual(
                _date_from_filename(test_case_input[i]), test_case_output[i]
            )

        # Random case
        for i in range(1000):
            name = random.choice(['위치 기록', 'Location History'])
            year = random.randint(0, 9999)
            month = random.choice(month_names[1:])
            month_number = month_names.index(month)
            self.assertEqual(
                _date_from_filename(template.format(name, year, year, month)),
                (year, month_number)
            )

if __name__ == '__main__':
    unittest.main()
