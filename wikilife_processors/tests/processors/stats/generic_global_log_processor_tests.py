# coding=utf-8

from wikilife_processors.tests.base_test import BaseTest
from wikilife_processors.utils.log_preprocessor import LogPreprocessor
from wikilife_processors.processors.stats.generic_global_log_processor import GenericGlobalLogProcessor, GenericGlobalLogProcessorException
from wikilife_utils.date_utils import DateUtils
import datetime


class GenericGlobalLogProcessorTests(BaseTest):
    
    _generic_global_log_stats_mgr = None
    _generic_global_log_stats_prc = None
    _generic_global_log_stats_db = None
    
    def setUp(self):
        self._generic_global_log_stats_db = self.get_db_conn().get_conn_processors().generic_global_log_stats
        logger = self.get_logger()
        
        managers = self.get_managers()
        log_pre_pro = LogPreprocessor(managers.meta_mgr)
        self._generic_global_log_stats_mgr = managers.generic_global_log_stats_mgr
        
        self._generic_global_log_stats_prc = GenericGlobalLogProcessor(logger, managers, log_pre_pro)

    def tearDown(self):
        self._generic_global_log_stats_db.remove({"date":"2011-07-15"})
        self._generic_global_log_stats_db = None
        self._generic_global_log_stats_mgr = None
        self._generic_global_log_stats_prc = None

        
    def test_accept_log(self):      
        log_option = self._get_log_option()
        log_range = self._get_log_range()
        assert self._generic_global_log_stats_prc.accept(log_option) == True
        assert self._generic_global_log_stats_prc.accept(log_range) == True

    
    def test_insert_range_log(self):
        log_range = self._get_log_range()
        self._generic_global_log_stats_prc.insert(log_range)
        loggable_id = "19"
        property_id = "20"
        value_node_id = "21"
        found_day = self._generic_global_log_stats_mgr.get_log_day("2011-07-15")
        
        assert loggable_id in found_day["log_nodes"]
        assert found_day["log_nodes"][loggable_id]["count"] == 1
        assert property_id in found_day["log_nodes"][loggable_id]
        assert found_day["log_nodes"][loggable_id][property_id]["count"] == 1
        assert value_node_id in found_day["log_nodes"][loggable_id][property_id]
        assert found_day["log_nodes"][loggable_id][property_id][value_node_id]["count"] == 1
        assert found_day["log_nodes"][loggable_id][property_id][value_node_id]["sum"] == 3
        assert len(found_day["log_nodes"][loggable_id][property_id][value_node_id]["option_sum"]) == 1
        
        for opt in  found_day["log_nodes"][loggable_id][property_id][value_node_id]["option_sum"]:
            assert opt["opt"] == 3
            assert opt["count"] == 1
            
    def test_insert_option_log(self):
        log_option = self._get_log_option()
        self._generic_global_log_stats_prc.insert(log_option)

        loggable_id = "11"
        property_id = "12"
        value_node_id = "13"
        found_day = self._generic_global_log_stats_mgr.get_log_day("2011-07-15")
        
        assert loggable_id in found_day["log_nodes"]
        assert found_day["log_nodes"][loggable_id]["count"] == 1
        assert property_id in found_day["log_nodes"][loggable_id]
        assert found_day["log_nodes"][loggable_id][property_id]["count"] == 1
        assert value_node_id in found_day["log_nodes"][loggable_id][property_id]
        assert found_day["log_nodes"][loggable_id][property_id][value_node_id]["count"] == 1
        assert len(found_day["log_nodes"][loggable_id][property_id][value_node_id]["option_sum"]) == 1
        for opt in found_day["log_nodes"][loggable_id][property_id][value_node_id]["option_sum"]:
            assert opt["opt"] == "yellow"
            assert opt["count"] == 1

        log_option = self._get_log_option()
        log_option["fields"]["nodes"][0]["value"] = "brown"
        self._generic_global_log_stats_prc.insert(log_option)
        
        found_day = self._generic_global_log_stats_mgr.get_log_day("2011-07-15")

        assert loggable_id in found_day["log_nodes"]
        assert found_day["log_nodes"][loggable_id]["count"] == 2
        assert property_id in found_day["log_nodes"][loggable_id]
        assert found_day["log_nodes"][loggable_id][property_id]["count"] == 2
        assert value_node_id in found_day["log_nodes"][loggable_id][property_id]
        assert found_day["log_nodes"][loggable_id][property_id][value_node_id]["count"] == 2
        assert len(found_day["log_nodes"][loggable_id][property_id][value_node_id]["option_sum"]) == 2
        for opt in found_day["log_nodes"][loggable_id][property_id][value_node_id]["option_sum"]:
            assert opt["count"] == 1
            

    def test_delete_option_log(self):
                
        log_option = self._get_log_option()
        self._generic_global_log_stats_prc.insert(log_option)
        self._generic_global_log_stats_prc.delete(log_option)
        found_day = self._generic_global_log_stats_mgr.get_log_day( "2011-07-15")
        assert found_day["log_nodes"] == {}
        
        self._generic_global_log_stats_prc.insert(log_option)
        self._generic_global_log_stats_prc.insert(log_option)
        self._generic_global_log_stats_prc.insert(log_option)
        self._generic_global_log_stats_prc.delete(log_option)

        loggable_id = "11"
        property_id = "12"
        value_node_id = "13"
        found_day = self._generic_global_log_stats_mgr.get_log_day("2011-07-15")
        
        assert loggable_id in found_day["log_nodes"]
        assert found_day["log_nodes"][loggable_id]["count"] == 2
        assert property_id in found_day["log_nodes"][loggable_id]
        assert found_day["log_nodes"][loggable_id][property_id]["count"] == 2
        assert value_node_id in found_day["log_nodes"][loggable_id][property_id]
        assert found_day["log_nodes"][loggable_id][property_id][value_node_id]["count"] == 2
        assert len(found_day["log_nodes"][loggable_id][property_id][value_node_id]["option_sum"]) == 1
        for opt in found_day["log_nodes"][loggable_id][property_id][value_node_id]["option_sum"]:
            assert opt["opt"] == "yellow"
            assert opt["count"] == 2

    def test_delete_range_log(self):
        log_range = self._get_log_range()
        self._generic_global_log_stats_prc.insert(log_range)
        self._generic_global_log_stats_prc.delete(log_range)
        found_day = self._generic_global_log_stats_mgr.get_log_day("2011-07-15")
        assert found_day["log_nodes"] == {}
        
        self._generic_global_log_stats_prc.insert(log_range)
        self._generic_global_log_stats_prc.insert(log_range)
        self._generic_global_log_stats_prc.insert(log_range)
        self._generic_global_log_stats_prc.delete(log_range)

        loggable_id = "19"
        property_id = "20"
        value_node_id = "21"
        found_day = self._generic_global_log_stats_mgr.get_log_day("2011-07-15")
        
        assert loggable_id in found_day["log_nodes"]
        assert found_day["log_nodes"][loggable_id]["count"] == 2
        assert property_id in found_day["log_nodes"][loggable_id]
        assert found_day["log_nodes"][loggable_id][property_id]["count"] == 2
        assert value_node_id in found_day["log_nodes"][loggable_id][property_id]
        assert found_day["log_nodes"][loggable_id][property_id][value_node_id]["count"] == 2
        assert found_day["log_nodes"][loggable_id][property_id][value_node_id]["sum"] == 6

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

