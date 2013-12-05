# coding=utf-8

from wikilife_processors.processors.stats.was.factors.factors_model import \
    GenderFactor
from wikilife_processors.tests.base_test import BaseTest


class GenderFactorTests(BaseTest):

    def test_process_value(self):
        factor = GenderFactor(values=[
                {"id": "female", "name": "Female", "value": "Female"},
                {"id": "male", "name": "Male", "value": "Male"}
            ])

        raw_value = "Female"
        value = factor.process_value(raw_value)

        assert value == raw_value
