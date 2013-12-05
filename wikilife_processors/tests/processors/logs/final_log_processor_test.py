# coding=utf-8

from wikilife_processors.tests.base_test import BaseTest
from wikilife_processors.processors.logs.final_log_processor import FinalLogProcessor, FinalLogException
from wikilife_data.managers.final_logs.final_log_manager import CREATE_DATETIME_UTC_FIELD
from wikilife_utils.date_utils import DateUtils
import datetime

TEST_USER_ID = "TEST"

class FinalLogProcessorTests(BaseTest):
    
    final_log_mgr = None
    final_prc = None

    def setUp(self):
        self._logs = self.get_db_conn().get_conn_processors().final_logs_test
        logger = self.get_logger()
        
        managers = self.get_managers()
        self.final_log_mgr = managers.final_log_mgr
        
        self.final_prc = FinalLogProcessor(logger, managers)

    def tearDown(self):
        self.get_db_conn().get_conn_processors().drop_collection("final_logs_test")      
        self._logs = None
        self._mgr = None

        
    def test_accept_log(self):      
        log = self._get_log()

        assert self.final_prc.accept(log) == True

  

    def test_insert(self):
        log = self._get_log()
        self.final_prc.insert(log)
        assert self.final_log_mgr.get_final_logs_count() == 1
        found_log = self.final_log_mgr.get_final_log_by_id(log["pk"])
        assert found_log["pk"] == log["pk"]
        assert found_log["user_id"] == log["fields"]["user_id"]
        assert found_log["source"] == log["fields"]["source"]
        assert found_log["execute_time"] == log["fields"]["execute_time"]

    def test_delete(self):
        
        
        try:
            self.final_prc.delete({"pk":200})
            assert False
        except FinalLogException:
            assert True
        
        log = self._get_log()
        assert self.final_log_mgr.get_final_logs_count() == 1
        self.final_prc.delete(log)
        assert self.final_log_mgr.get_final_logs_count() == 0

    """ helpers """

    def _get_log(self):
        return {u'pk': 36, u'model': u'LogEntry', 'create_datetime_utc':datetime.datetime(2011, 7, 15, 15, 19, 31),
                  u'fields': {u'status': 1, u'execute_time_utc': datetime.datetime(2011, 7, 15, 15, 19, 31), 
                              u'server_id': 36, u'user_id': u'DG3NQF', u'client_id': 15, u'update_date': u'2011-07-15', u'text': u'Desperate Moderate', 
                              u'create_time_utc': datetime.datetime(2011, 7, 15, 18, 10, 58, 911000), u'execute_date': u'2011-07-15', 
                              u'update_time': u'2011-07-15 18:10:58 +0000', u'execute_time': u'2011-07-15 15:19:31 +0000', u'source': u'client.iphone', 
                              u'original_entry': 0, u'create_time': u'2011-07-15 18:10:58 +0000', u'root_slug': u'healthcare', u'create_date': u'2011-07-15',
                               u'nodes': [{u'node_namespace': u'wikilife.mood.mood-list.desperate.intensity.value-node', u'node_id': 1090, u'value': 3, u'title': u'Desperate'}], 
                               u'user_log': 1}}

