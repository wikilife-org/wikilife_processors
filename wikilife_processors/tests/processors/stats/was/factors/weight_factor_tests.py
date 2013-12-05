# coding=utf-8

from wikilife_processors.tests.base_test import BaseTest
from wikilife_processors.processors.stats.was.factors.factors_model import WeightFactor


class WeightFactorTests(BaseTest):

    def test_process_value(self):
        factor = WeightFactor(values=[
            {"id": "lt40", "name": "less than 40", "min": 0, "max": 40},
            {"id": "40-50", "name": "41 to 50", "min": 40, "max": 50},
            {"id": "50-60", "name": "51 to 60", "min": 50, "max": 60},
            {"id": "60-70", "name": "61 to 70", "min": 60, "max": 70},
            {"id": "70-80", "name": "71 to 80", "min": 70, "max": 80},
            {"id": "80-90", "name": "81 to 90", "min": 80, "max": 90},
            {"id": "90-110", "name": "91 to 110", "min": 90, "max": 110},
            {"id": "110-130", "name": "111 to 130", "min": 110, "max": 130},
            {"id": "130-150", "name": "131 to 150", "min": 130, "max": 150},
            {"id": "gt150", "name": "more than 150", "min": 150, "max": None}
        ])

        raw_value = 75
        value = factor.process_value(raw_value)
        assert value == raw_value
