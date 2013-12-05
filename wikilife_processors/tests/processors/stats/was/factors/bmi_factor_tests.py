# coding=utf-8

from wikilife_processors.tests.base_test import BaseTest
from wikilife_processors.processors.stats.was.factors.factors_model import BMIFactor
from wikilife_data.managers.profile.profile_manager import WEIGHT_ITEM,\
    HEIGHT_ITEM


HEIGHT_NODE_ID = 1
WEIGHT_NODE_ID = 2
EXISTING_USER_ID = "Test"
INCOMPLETE_USER_ID = "incomplete"
NOT_EXISTING_USER_ID = "fake"

class BMIFactorTests(BaseTest):

    def test_process_value(self):
        daos = MockDAOs() 

        factor = BMIFactor(daos=daos, height_node_id=HEIGHT_NODE_ID, weight_node_id=WEIGHT_NODE_ID, values=[
                {"id": "lt16", "name": "less than 16.00", "min": 0, "max": 16},
                {"id": "16-185", "name": "16.00 to 18.50", "min": 16, "max": 18.5},
                {"id": "50-60", "name": "18.50 to 24.99", "min": 18.5, "max": 24.99},
                {"id": "60-70", "name": "25 to 29.99", "min": 25, "max": 29.99},
                {"id": "70-80", "name": "30 to 34.99", "min": 30, "max": 34.99},
                {"id": "80-90", "name": "35 to 39.99", "min": 35, "max": 39.99},
                {"id": "gt40", "name": "more than 40", "min": 40, "max": None}
            ])

        user_id = EXISTING_USER_ID

        node_id = HEIGHT_NODE_ID
        raw_value = 1.8
        value = factor.process_value(raw_value, user_id, node_id)
        assert value == 70.0/(raw_value*raw_value)

        node_id = WEIGHT_NODE_ID
        raw_value = 75
        value = factor.process_value(raw_value, user_id, node_id)
        assert value == raw_value*1.0/(1.7*1.7)

        node_id = 3
        raw_value = 75
        value = factor.process_value(raw_value, user_id, node_id)
        assert value == None

    def test_process_value_bad_user(self):
        daos = MockDAOs() 

        factor = BMIFactor(daos=daos, height_node_id=HEIGHT_NODE_ID, weight_node_id=WEIGHT_NODE_ID, values=[
                {"id": "lt16", "name": "less than 16.00", "min": 0, "max": 16},
                {"id": "16-185", "name": "16.00 to 18.50", "min": 16, "max": 18.5},
                {"id": "50-60", "name": "18.50 to 24.99", "min": 18.5, "max": 24.99},
                {"id": "60-70", "name": "25 to 29.99", "min": 25, "max": 29.99},
                {"id": "70-80", "name": "30 to 34.99", "min": 30, "max": 34.99},
                {"id": "80-90", "name": "35 to 39.99", "min": 35, "max": 39.99},
                {"id": "gt40", "name": "more than 40", "min": 40, "max": None}
            ])

        user_id = NOT_EXISTING_USER_ID

        node_id = HEIGHT_NODE_ID
        raw_value = 1.8
        value = factor.process_value(raw_value, user_id, node_id)
        assert value == None

    def test_process_value_incomplete_profile(self):
        daos = MockDAOs() 

        factor = BMIFactor(daos=daos, height_node_id=HEIGHT_NODE_ID, weight_node_id=WEIGHT_NODE_ID, values=[
                {"id": "lt16", "name": "less than 16.00", "min": 0, "max": 16},
                {"id": "16-185", "name": "16.00 to 18.50", "min": 16, "max": 18.5},
                {"id": "50-60", "name": "18.50 to 24.99", "min": 18.5, "max": 24.99},
                {"id": "60-70", "name": "25 to 29.99", "min": 25, "max": 29.99},
                {"id": "70-80", "name": "30 to 34.99", "min": 30, "max": 34.99},
                {"id": "80-90", "name": "35 to 39.99", "min": 35, "max": 39.99},
                {"id": "gt40", "name": "more than 40", "min": 40, "max": None}
            ])

        user_id = INCOMPLETE_USER_ID

        node_id = HEIGHT_NODE_ID
        raw_value = 1.8
        value = factor.process_value(raw_value, user_id, node_id)
        assert value == None


class MockProfileDAO(object):
    def get_profile_by_user_id(self, user_id):
        
        profile = None
        
        if user_id==EXISTING_USER_ID:
            profile = {}
            profile["items"] = {}
            profile["items"][WEIGHT_ITEM] = {"node_id": WEIGHT_NODE_ID,   "value": 70.0}
            profile["items"][HEIGHT_ITEM] = {"node_id": HEIGHT_ITEM,   "value": 1.7}
        
        elif user_id==EXISTING_USER_ID:
            profile = {}
            profile["items"] = {}
            profile["items"][WEIGHT_ITEM] = {"node_id": WEIGHT_NODE_ID,   "value": None}
            profile["items"][HEIGHT_ITEM] = {"node_id": HEIGHT_ITEM,   "value": None}

        return profile


class MockDAOs(object):
    profile_mgr = MockProfileDAO()
