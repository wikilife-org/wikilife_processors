# coding=utf-8

from wikilife_processors.tests.base_test import BaseTest
from wikilife_processors.processors.stats.user_log_processor import UserLogProcessor, UserLogProcessorException
from wikilife_utils.date_utils import DateUtils
import datetime

TEST_USER_ID = "TEST"

class UserLogProcessorTests(BaseTest):
    
    user_log_stats_mgr = None
    user_log_stats_prc = None
    
    def setUp(self):
        self._user_log_stats_db = self.get_db_conn().get_conn_processors().user_log_stats
        logger = self.get_logger()
        
        managers = self.get_managers()
        self.user_log_stats_mgr = managers.user_log_stats_mgr
        
        self.user_log_stats_prc = UserLogProcessor(logger, managers)

    def tearDown(self):
        self._user_log_stats_db.remove({"user_id":"TEST"})
        self._user_log_stats_db = None
        self.user_log_stats_mgr = None
        self.user_log_stats_prc = None

        
    def test_accept_log(self):      
        log_option = self._get_log_option()
        log_range = self._get_log_range()
        assert self.user_log_stats_prc.accept(log_option) == True
        assert self.user_log_stats_prc.accept(log_range) == True

    
    def test_insert_range_log(self):
        log_range = self._get_log_range()
        self.user_log_stats_prc.insert(log_range)
        loggable_id = "19"
        property_id = "20"
        value_node_id = "21"
        found_user_log_day = self.user_log_stats_mgr.get_user_log_day("TEST", "2011-07-15")
        
        assert loggable_id in found_user_log_day["log_nodes"]
        assert found_user_log_day["log_nodes"][loggable_id]["count"] == 1
        assert property_id in found_user_log_day["log_nodes"][loggable_id]
        assert found_user_log_day["log_nodes"][loggable_id][property_id]["count"] == 1
        assert value_node_id in found_user_log_day["log_nodes"][loggable_id][property_id]
        assert found_user_log_day["log_nodes"][loggable_id][property_id][value_node_id]["count"] == 1
        assert found_user_log_day["log_nodes"][loggable_id][property_id][value_node_id]["sum"] == 3
        
    
    def test_insert_option_log(self):
        log_option = self._get_log_option()
        self.user_log_stats_prc.insert(log_option)

        loggable_id = "11"
        property_id = "12"
        value_node_id = "13"
        found_user_log_day = self.user_log_stats_mgr.get_user_log_day("TEST", "2011-07-15")
        
        assert loggable_id in found_user_log_day["log_nodes"]
        assert found_user_log_day["log_nodes"][loggable_id]["count"] == 1
        assert property_id in found_user_log_day["log_nodes"][loggable_id]
        assert found_user_log_day["log_nodes"][loggable_id][property_id]["count"] == 1
        assert value_node_id in found_user_log_day["log_nodes"][loggable_id][property_id]
        assert found_user_log_day["log_nodes"][loggable_id][property_id][value_node_id]["count"] == 1
        assert len(found_user_log_day["log_nodes"][loggable_id][property_id][value_node_id]["option_sum"]) == 1
        for opt in found_user_log_day["log_nodes"][loggable_id][property_id][value_node_id]["option_sum"]:
            assert opt["opt"] == "yellow"
            assert opt["count"] == 1

        log_option = self._get_log_option()
        log_option["fields"]["nodes"][0]["value"] = "brown"
        self.user_log_stats_prc.insert(log_option)
        
        found_user_log_day = self.user_log_stats_mgr.get_user_log_day("TEST", "2011-07-15")

        assert loggable_id in found_user_log_day["log_nodes"]
        assert found_user_log_day["log_nodes"][loggable_id]["count"] == 2
        assert property_id in found_user_log_day["log_nodes"][loggable_id]
        assert found_user_log_day["log_nodes"][loggable_id][property_id]["count"] == 2
        assert value_node_id in found_user_log_day["log_nodes"][loggable_id][property_id]
        assert found_user_log_day["log_nodes"][loggable_id][property_id][value_node_id]["count"] == 2
        assert len(found_user_log_day["log_nodes"][loggable_id][property_id][value_node_id]["option_sum"]) == 2
        for opt in found_user_log_day["log_nodes"][loggable_id][property_id][value_node_id]["option_sum"]:
            assert opt["count"] == 1
            

    def test_delete_option_log(self):
                
        log_option = self._get_log_option()
        self.user_log_stats_prc.insert(log_option)
        self.user_log_stats_prc.delete(log_option)
        found_user_log_day = self.user_log_stats_mgr.get_user_log_day("TEST", "2011-07-15")
        assert found_user_log_day["log_nodes"] == {}
        
        self.user_log_stats_prc.insert(log_option)
        self.user_log_stats_prc.insert(log_option)
        self.user_log_stats_prc.insert(log_option)
        self.user_log_stats_prc.delete(log_option)

        loggable_id = "11"
        property_id = "12"
        value_node_id = "13"
        found_user_log_day = self.user_log_stats_mgr.get_user_log_day("TEST", "2011-07-15")
        
        assert loggable_id in found_user_log_day["log_nodes"]
        assert found_user_log_day["log_nodes"][loggable_id]["count"] == 2
        assert property_id in found_user_log_day["log_nodes"][loggable_id]
        assert found_user_log_day["log_nodes"][loggable_id][property_id]["count"] == 2
        assert value_node_id in found_user_log_day["log_nodes"][loggable_id][property_id]
        assert found_user_log_day["log_nodes"][loggable_id][property_id][value_node_id]["count"] == 2
        assert len(found_user_log_day["log_nodes"][loggable_id][property_id][value_node_id]["option_sum"]) == 1
        for opt in found_user_log_day["log_nodes"][loggable_id][property_id][value_node_id]["option_sum"]:
            assert opt["opt"] == "yellow"
            assert opt["count"] == 2

    def test_delete_range_log(self):
        log_range = self._get_log_range()
        self.user_log_stats_prc.insert(log_range)
        self.user_log_stats_prc.delete(log_range)
        found_user_log_day = self.user_log_stats_mgr.get_user_log_day("TEST", "2011-07-15")
        assert found_user_log_day["log_nodes"] == {}
        
        self.user_log_stats_prc.insert(log_range)
        self.user_log_stats_prc.insert(log_range)
        self.user_log_stats_prc.insert(log_range)
        self.user_log_stats_prc.delete(log_range)

        loggable_id = "19"
        property_id = "20"
        value_node_id = "21"
        found_user_log_day = self.user_log_stats_mgr.get_user_log_day("TEST", "2011-07-15")
        
        assert loggable_id in found_user_log_day["log_nodes"]
        assert found_user_log_day["log_nodes"][loggable_id]["count"] == 2
        assert property_id in found_user_log_day["log_nodes"][loggable_id]
        assert found_user_log_day["log_nodes"][loggable_id][property_id]["count"] == 2
        assert value_node_id in found_user_log_day["log_nodes"][loggable_id][property_id]
        assert found_user_log_day["log_nodes"][loggable_id][property_id][value_node_id]["count"] == 2
        assert found_user_log_day["log_nodes"][loggable_id][property_id][value_node_id]["sum"] == 6

    """ helpers """

    def _get_log_option(self):
        return {u'pk': 36, u'model': u'LogEntry', 'create_datetime_utc':datetime.datetime(2011, 7, 15, 15, 19, 31),
                  u'fields': {u'status': 1, u'execute_time_utc': datetime.datetime(2011, 7, 15, 15, 19, 31), 
                              u'server_id': 36, u'user_id': u'TEST', u'client_id': 15, u'update_date': u'2011-07-15', u'text': u'Pee yellow', 
                              u'create_time_utc': datetime.datetime(2011, 7, 15, 18, 10, 58, 911000), u'execute_date': u'2011-07-15', 
                              u'update_time': u'2011-07-15 18:10:58 +0000', u'execute_time': u'2011-07-15 15:19:31 +0000', u'source': u'client.iphone', 
                              u'original_entry': 0, u'create_time': u'2011-07-15 18:10:58 +0000', u'root_slug': u'physiological', u'create_date': u'2011-07-15',
                               u'nodes': [{u'node_namespace': u'wikilife.physiological.pee.color.value-node', u'node_id': 13, u'value': "yellow", "property_id": "12", "loggable_id":"11"}], 
                               u'user_log': 1}}
        
    def _get_log_range(self):
        return  {u'pk': 37, u'model': u'LogEntry', 'create_datetime_utc':datetime.datetime(2011, 7, 15, 15, 19, 31),
                  u'fields': {u'status': 1, u'execute_time_utc': datetime.datetime(2011, 7, 15, 15, 19, 31), 
                              u'server_id': 36, u'user_id': u'TEST', u'client_id': 15, u'update_date': u'2011-07-15', u'text': u'Cannabis 3', 
                              u'create_time_utc': datetime.datetime(2011, 7, 15, 18, 10, 58, 911000), u'execute_date': u'2011-07-15', 
                              u'update_time': u'2011-07-15 18:10:58 +0000', u'execute_time': u'2011-07-15 15:19:31 +0000', u'source': u'client.iphone', 
                              u'original_entry': 0, u'create_time': u'2011-07-15 18:10:58 +0000', u'root_slug': u'leisure', u'create_date': u'2011-07-15',
                               u'nodes': [{u'node_namespace': u'wikilife.leisure.smoking.cannabis.quantity.value-node', u'node_id': 21, u'value': 3,"property_id": "20", "loggable_id":"19"}], 
                               u'user_log': 1}}

