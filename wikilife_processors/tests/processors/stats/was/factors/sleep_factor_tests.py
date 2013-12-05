# coding=utf-8

from wikilife_processors.processors.stats.was.factors.factors_model import \
    SleepFactor
from wikilife_processors.tests.base_test import BaseTest
from wikilife_utils.date_utils import DateUtils


class SleepFactorTests(BaseTest):
    """
    Further testing on super class DailySumAvgFactor
    """

    _daos = None
    
    def setUp(self):
        self._daos = self.get_service_builder().build_managers()
        try:
            self._daos.aggregation_profile_vars_dao._collection.drop()
        except: pass
    
    def tearDown(self):
        try:
            self._daos.aggregation_profile_vars_dao._collection.drop()
        except: pass

    def test_process_value(self):
        factor = SleepFactor(daos=self._daos, values=[
            {"id": "lt6", "name": "less than 6", "min": 0, "max": 6},
            {"id": "6-8", "name": "6 to 8", "min": 6, "max": 8},
            {"id": "gt8", "name": "more than 8", "min": 8, "max": None}
        ])
        
        user_id = "TEST_SleepFactor"
        node_id = 123

        exec_date = DateUtils.get_datetime_utc()

        raw_value = 8*60
        expected_value = 8
        processed_value = factor.process_value(raw_value=raw_value, user_id=user_id, node_id=node_id, exec_date=exec_date)
        self.assertEquals(processed_value, expected_value)

        raw_value = 9*60
        expected_value = 8+9
        processed_value = factor.process_value(raw_value=raw_value, user_id=user_id, node_id=node_id, exec_date=exec_date)
        self.assertEquals(processed_value, expected_value)

        exec_date = DateUtils.add_days(exec_date, -1)
        
        raw_value = 10*60
        expected_value = (8+9 + 10)/2.0
        processed_value = factor.process_value(raw_value=raw_value, user_id=user_id, node_id=node_id, exec_date=exec_date)
        self.assertEquals(processed_value, expected_value)
