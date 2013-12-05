# coding=utf-8

from wikilife_processors.processors.stats.was.factors.aggregation_factors import \
    AggregationFactors
from wikilife_processors.tests.base_test import BaseTest
from wikilife_utils.date_utils import DateUtils


TEST_USER_ID = "TEST_AF"

class AggregationFactorsTests(BaseTest):

    _aggregation_factors = None

    def setUp(self):
        daos = self.get_service_builder().build_managers()
        try:
            daos.aggregation_profile_vars_dao._collection.drop()
        except: pass
        self._aggregation_factors = AggregationFactors(daos)
    
    def test_get_factors(self):
        for factor in self._aggregation_factors.get_factors():
            print factor.id

        assert True
    
    def test_get_by_factor_id(self):
        for factor in self._aggregation_factors.get_factors():
            assert self._aggregation_factors.get_by_factor_id(factor.id) == factor

    def test_get_node_ids(self):
        print self._aggregation_factors.get_node_ids()
        assert True

    def test_create_blank_profile_factors(self):
        print self._aggregation_factors.create_blank_profile_factors()
        assert True

    def test_update_profile_factors(self):
        """
        class GenderFactor(Factor):
            def __init__(self, values):
                Factor.__init__(self, id="gender", name="Gender", value_type=Factor.OPTION, values=values)
        
        self._add_factor(1159, 
            GenderFactor(values=[
                {"id": "female", "name": "Female", "value": "Female"},
                {"id": "male", "name": "Male", "value": "Male"}
            ])
        )
        """
        profile_factors = {"gender": None, "age": None, "weight": None}
        expected_profile_factors = {"gender": "Female", "age": None, "weight": None}
        updated_profile_factors = self._aggregation_factors.update_profile_factors(profile_factors, "gender", "Female")
        self.assertEquals(updated_profile_factors, expected_profile_factors)

    def test_process_value(self):
        user_id = TEST_USER_ID
        f_id = "gender"
        node_id = 1159
        exec_date = DateUtils.get_datetime_utc()
        raw_value = "Female"
        factor_id, value = self._aggregation_factors.process_value(raw_value=raw_value, user_id=user_id, node_id=node_id, exec_date=exec_date)
        assert factor_id == f_id
        assert value == raw_value
