# coding=utf-8
import datetime

from wikilife_processors.tests.base_test import BaseTest
from wikilife_processors.tests.processors.base_processor_tests import BaseProcessorTests

from wikilife_utils.stats_utils import StatsUtils

from wikilife_processors.processors.stats.log_category_process import LogCategoryProcess

class LogCategoryProcessTests(BaseProcessorTests):

    db = None    
    log_cate_prc = None
    stats_mgr = None
    logger = None

    def setUp(self):
        self.db = self.get_conn().test_generic_daily_stats
        self.get_conn().drop_database("test_generic_daily_stats")
        
        logger = self.get_logger()
        
        mgr_locator = self.get_mgr_locator(self.db)
        self.stats_mgr = mgr_locator.stats_mgr
        #Ver managers y sus conexiones.
        self.meta_mgr = mgr_locator.meta_mgr
        self.report_mgr = mgr_locator.reports_mgr
        
        self.meds_prc = LogCategoryProcess(logger, mgr_locator)

    def tearDown(self):
        self.get_conn().drop_database("test_generic_daily_stats")

    def test_insert(self):
        pass
    
    def test_delete(self):
        pass

            
    """ helpers """

    def _get_valid_log(self):
        log =  {u'pk': 36, 
                u'model': u'LogEntry', 
                u'fields': {u'status': 1, 
                                u'server_id': 36, 
                                u'user_id': u'DG3NQF', 
                                u'client_id': 15, 
                                u'text': u'XXXXX', 
                                u'execute_time': u'2011-07-15 15:19:31 +0000', 
                                u'original_entry': 0,
                                u'root_slug': u'healthcare', 
                                 u'nodes': [{u'node_namespace': u'wikilife.healthcare.drug.phenelzine-sulfate-tablet.strength.value-node', u'node_id': 316756, u'value': "1000 ml"}], u'user_log': 1}}
        return log
    
    def _get_delete_log(self):
        log =  {u'pk': 36, 
                u'model': u'LogEntry', 
                u'fields': {u'status': 1, 
                                u'server_id': 36, 
                                u'user_id': u'DG3NQF', 
                                u'client_id': 15, 
                                u'text': u'XXXX', 
                                u'execute_time': u'2011-07-15 13:12:12 +0000', 
                                u'original_entry': 0,
                                u'root_slug': u'healthcare', 
                                 u'nodes': [{u'node_namespace': u'wikilife.healthcare.drug.phenelzine-sulfate-tablet.strength.value-node', u'node_id': 316776, u'value': "400 ml"}], u'user_log': 1}}
        return log
    
    def _get_invalid_log(self):
        log =  {u'pk': 36, 
                u'model': u'LogEntry', 
                u'fields': {u'status': 1, 
                                u'server_id': 36, 
                                u'user_id': u'DG3NQF', 
                                u'client_id': 15, 
                                u'text': u'XXXX', 
                                u'execute_time': u'2011-07-15 15:19:31 +0000', 
                                u'original_entry': 0,
                                u'root_slug': u'healthcare', 
                                 u'nodes': [{u'node_namespace': u'wikilife.mood.mood-list.happy.intensity.value-node', u'node_id': 251339, u'value': 3}], u'user_log': 1}}
        return log
    
   
        