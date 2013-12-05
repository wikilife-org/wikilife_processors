# coding=utf-8

from wikilife_processors.processors.stats.was.factors.factors_model import \
    LivingWithFactor
from wikilife_processors.tests.base_test import BaseTest


class LocationFactorTests(BaseTest):

    def test_process_value(self):
        factor = LivingWithFactor(values=[
                {"id": "alone", "name": "Alone", "value": "Alone"},
                {"id": "parents", "name": "Parents", "value": "With my parents"},
                {"id": "roomate", "name": "Roomate", "value": "With a roommate"},
                {"id": "children", "name": "Children", "value": "With my children"}
            ], 
             other_value={"id": "other", "name": "Other", "value": "Other"}
            )

        raw_value = "With a roommate"
        value = factor.process_value(raw_value)
        assert value == raw_value

        raw_value = "__ Option not defined"
        value = factor.process_value(raw_value)
        assert value == "Other"
