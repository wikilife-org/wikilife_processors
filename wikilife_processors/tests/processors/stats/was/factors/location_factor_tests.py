# coding=utf-8

from wikilife_processors.tests.base_test import BaseTest
from wikilife_processors.processors.stats.was.factors.factors_model import LocationFactor


class LocationFactorTests(BaseTest):

    def test_process_value(self):
        factor = LocationFactor(values=[
                {"id": "newyork", "name": "New York", "value": "New York"},
                {"id": "sanfrancisco", "name": "San Francisco", "value": "San Francisco"},
                {"id": "buenosaires", "name": "Buenos Aires", "value": "Buenos Aires"},
                {"id": "london", "name": "London", "value": "London"}
            ], 
            other_value={"id": "other", "name": "Other", "value": "Other"}
            )
        
        raw_value = "San Francisco"
        value = factor.process_value(raw_value)
        assert value == raw_value

        raw_value = "__ Option not defined"
        value = factor.process_value(raw_value)
        assert value == "Other"
