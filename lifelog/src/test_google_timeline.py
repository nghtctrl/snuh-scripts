#!/usr/bin/env python

import unittest
import random
import os
from pprint import pprint

import google_timeline

class TestGoogleTimeline(unittest.TestCase):
    def test_xor(self):
        self.assertEqual(google_timeline._xor(True, True), False)
        self.assertEqual(google_timeline._xor(True, False), True)
        self.assertEqual(google_timeline._xor(False, True), True)
        self.assertEqual(google_timeline._xor(False, False), False)

    def test_get_date(self):
        template_path = os.path.join('Takeout', '{}', 'Semantic Location History', '{}', '{}_{}.json')
        names = ['위치 기록', 'Location History']

        test_input = [
            template_path.format('위치 기록', '2021', '2021', 'SEPTEMBER'),
            template_path.format('위치 기록', '2021', '2021', 'OCTOBER'),
            template_path.format('위치 기록', '2021', '2021', 'NOVEMBER'),
            template_path.format('위치 기록', '2021', '2021', 'DECEMBER'),
            template_path.format('위치 기록', '2022', '2022', 'JANUARY'),
            template_path.format('위치 기록', '2022', '2022', 'FEBRUARY')
        ]

        test_output = [
            (2021, 9),
            (2021, 10),
            (2021, 11),
            (2021, 12),
            (2022, 1),
            (2022, 2),
        ]

        # Special test case
        for i in range(len(test_input)):
            self.assertEqual(
                google_timeline._get_date(test_input[i]), test_output[i]
            )

        # Random test case
        for i in range(1000):
            year = random.randint(0, 9999)
            month = random.choice(google_timeline.MONTH_NAMES[1:])
            month_number = google_timeline.MONTH_NAMES.index(month)
            self.assertEqual(
                google_timeline._get_date(template_path.format(random.choice(names), year, year, month)),
                (year, month_number)
            )

    def test_sort(self):
        template_path = os.path.join('Takeout', '{}', 'Semantic Location History', '{}', '{}_{}.json')

        unsorted_test_case_1 = [
            template_path.format('위치 기록', '2021', '2021', 'SEPTEMBER'),
            template_path.format('위치 기록', '2021', '2021', 'OCTOBER'),
            template_path.format('위치 기록', '2021', '2021', 'NOVEMBER'),
            template_path.format('위치 기록', '2021', '2021', 'DECEMBER'),
            template_path.format('위치 기록', '2022', '2022', 'JANUARY'),
            template_path.format('위치 기록', '2022', '2022', 'FEBRUARY')
        ]

        correct_output_1 = list(reversed(unsorted_test_case_1))

        sorted_test_case_1 = google_timeline._sort(unsorted_test_case_1)
        
        # Special test case
        for i in range(len(sorted_test_case_1)):
            self.assertEqual(correct_output_1[i] == sorted_test_case_1[i], True)

        # Generate a randomly shuffled list of paths
        unsorted_test_case_2 = sorted([
            template_path.format('위치 기록', year, year, google_timeline.MONTH_NAMES[i])
            for year in ['2020', '2021', '2022', '2023'] 
            for i in range(1, 13)
        ], key=lambda x: random.random())

        # Generate the correct output
        correct_output_2 = [
            template_path.format('위치 기록', year, year, google_timeline.MONTH_NAMES[i]) 
            for year in ['2023', '2022', '2021', '2020'] 
            for i in range(12, 0, -1)
        ]

        sorted_test_case_2 = google_timeline._sort(unsorted_test_case_2)

        # Random test case
        for i in range(len(sorted_test_case_2)):
            self.assertEqual(correct_output_2[i] == sorted_test_case_2[i], True)

if __name__ == '__main__':
    unittest.main()
