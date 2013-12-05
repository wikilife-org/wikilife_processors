# coding=utf-8

from wikilife_processors.tests.base_test import BaseTest
from wikilife_utils.date_utils import DateUtils
import random


AGGR_PRC_ID = "wikilife_processors.processors.stats.was.aggregation_processor.AggregationProcessor"

TEST_USER_BASE_ID = "TEST_L_"


class AggregationProcessorLargeTests(BaseTest):

    _daos = None

    def setUp(self):
        self._daos = self.get_service_builder().build_managers()
        try:
            self._daos.aggregation_profile_vars_dao._collection.drop()
            self._daos.aggregation_profile_dao._collection.drop()
            self._daos.aggregation_dao._collection.drop()
        except: pass

    def tearDown(self):
        try:
            self._daos.aggregation_profile_vars_dao._collection.drop()
            self._daos.aggregation_profile_dao._collection.drop()
            self._daos.aggregation_dao._collection.drop()
        except: pass
        

    def test_insert_mixed_large_data(self):
        prc = self.get_prc_builder().build_processor(AGGR_PRC_ID)

        genders = ["Male", "Female"]

        #users
        for i in range(1, 100):
            user_id = "%s%s" %(TEST_USER_BASE_ID, i)
            gender = genders[random.randint(0, 1)]
            log_nodes = [{"node_id": 1159, "value": gender}]
            log = self.create_final_log(user_id=user_id, log_nodes=log_nodes, start=DateUtils.get_datetime_utc())
            prc.insert(log, log["nodes"])
            
            birthdate = "%s-01-15 12:00:00 -0300" %random.randint(1930, 2000)
            log_nodes = [{"node_id": 1157, "value": birthdate}]
            log = self.create_final_log(user_id=user_id, log_nodes=log_nodes, start=DateUtils.get_datetime_utc())
            prc.insert(log, log["nodes"])

            #user last month sleep logs
            sleep_min = random.randint(4, 9)
            sleep_max = sleep_min + 3
            run_min = random.randint(1, 20)
            run_max = run_min + 5

            for x in range(-30, 0):
                exec_date = DateUtils.add_days(DateUtils.get_datetime_utc(), x)
                
                #Sleep
                log_nodes = [{"node_id": 241563, "value": random.randint(sleep_min, sleep_max)}]
                log = self.create_final_log(user_id=user_id, log_nodes=log_nodes, start=exec_date)
                prc.insert(log, log["nodes"])

                #Running
                log_nodes = [{"node_id": 241561, "value": random.randint(run_min, run_max)}]
                log = self.create_final_log(user_id=user_id, log_nodes=log_nodes, start=exec_date)
                prc.insert(log, log["nodes"])
