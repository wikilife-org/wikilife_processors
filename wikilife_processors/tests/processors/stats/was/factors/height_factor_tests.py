# coding=utf-8

from wikilife_processors.tests.base_test import BaseTest
from wikilife_processors.processors.stats.was.factors.factors_model import HeightFactor


class HeightFactorTests(BaseTest):

    def test_process_value(self):
        factor = HeightFactor(values=[
            {"id": "lt1", "name": "less than 1.00", "min": 0.0, "max": 1.0},
            {"id": "100-130", "name": "1.00 to 1.30", "min": 1.0, "max": 1.3},
            {"id": "131-150", "name": "1.31 to 1.50", "min": 1.31, "max": 1.5},
            {"id": "151-160", "name": "1.51 to 1.60", "min": 1.51, "max": 1.6},
            {"id": "161-170", "name": "1.61 to 1.70", "min": 1.61, "max": 1.7},
            {"id": "171-180", "name": "1.71 to 1.80", "min": 1.71, "max": 1.8},
            {"id": "181-190", "name": "1.81 to 1.90", "min": 1.81, "max": 1.9},
            {"id": "gt190", "name": "more than 1.90", "min": 1.9, "max": None}
        ])

        raw_value = 1.72
        value = factor.process_value(raw_value)
        assert value == raw_value
