# coding=utf-8

from wikilife_processors.processors.stats.was.factors.factors_model import \
    AgeFactor
from wikilife_processors.tests.base_test import BaseTest


class AgeFactorTests(BaseTest):

    def test_process_value(self):
        factor = AgeFactor(values=[
                {"id": "lt18", "name": "less than 18", "min": 0, "max": 18},
                {"id": "18-100", "name": "18 to 100", "min": 18, "max": 100},
                {"id": "gt100", "name": "more than 100", "min": 100, "max": None}
            ])
        
        raw_value = "1980-01-30"
        value = factor.process_value(raw_value)

        assert value == 33
