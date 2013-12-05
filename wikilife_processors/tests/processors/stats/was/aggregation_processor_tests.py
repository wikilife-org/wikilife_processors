# coding=utf-8

from wikilife_processors.tests.base_test import BaseTest
from wikilife_utils.date_utils import DateUtils


AGGR_PRC_ID = "wikilife_processors.processors.stats.was.aggregation_processor.AggregationProcessor"
TEST_USER_ID = "TEST1"


class AggregationProcessorTests(BaseTest):

    def test_accept_log(self):
        prc = self.get_prc_builder().build_processor(AGGR_PRC_ID)

        log_nodes = [{"node_id": 1157}]
        log = self.create_final_log(log_nodes=log_nodes)
        assert prc.accept(log) == (True, log_nodes)

        log_nodes = [{"node_id": 1159}]
        log = self.create_final_log(log_nodes=log_nodes)
        assert prc.accept(log) == (True, log_nodes)

        log_nodes = [{"node_id": 241563}]
        log = self.create_final_log(log_nodes=log_nodes)
        assert prc.accept(log) == (True, log_nodes)

    def test_insert_gender(self):
        prc = self.get_prc_builder().build_processor(AGGR_PRC_ID)

        log_nodes = [{"node_id": 1159, "value": "Male"}]
        log = self.create_final_log(user_id=TEST_USER_ID, log_nodes=log_nodes, start=DateUtils.get_datetime_utc())
        prc.insert(log, log["nodes"])
        assert True

        log_nodes = [{"node_id": 1159, "value": "Female"}]
        log = self.create_final_log(user_id=TEST_USER_ID, log_nodes=log_nodes, start=DateUtils.get_datetime_utc())
        prc.insert(log, log["nodes"])
        assert True

    def test_insert_age(self):
        prc = self.get_prc_builder().build_processor(AGGR_PRC_ID)

        log_nodes = [{"node_id": 1157, "value": "1980-01-15 12:00:00 -0300"}]
        log = self.create_final_log(user_id=TEST_USER_ID, log_nodes=log_nodes, start=DateUtils.get_datetime_utc())
        prc.insert(log, log["nodes"])
        assert True

        log_nodes = [{"node_id": 1157, "value": "1985-01-15 12:00:00 -0300"}]
        log = self.create_final_log(user_id=TEST_USER_ID, log_nodes=log_nodes, start=DateUtils.get_datetime_utc())
        prc.insert(log, log["nodes"])
        assert True

    def test_insert_sleep(self):
        prc = self.get_prc_builder().build_processor(AGGR_PRC_ID)

        log_nodes = [{"node_id": 241563, "value": 4.5}]
        log = self.create_final_log(user_id=TEST_USER_ID, log_nodes=log_nodes, start=DateUtils.get_datetime_utc())
        prc.insert(log, log["nodes"])
        assert True
        
        log_nodes = [{"node_id": 241563, "value": 2}]
        log = self.create_final_log(user_id=TEST_USER_ID, log_nodes=log_nodes, start=DateUtils.get_datetime_utc())
        prc.insert(log, log["nodes"])
        assert True
