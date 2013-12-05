# coding=utf-8
import datetime

from wikilife_processors.tests.base_test import BaseTest
from wikilife_processors.tests.processors.base_processor_tests import BaseProcessorTests

from wikilife_utils.stats_utils import StatsUtils

from wikilife_processors.processors.stats.medical_visit_processor import MedicalVisitProcessor

class MedicalVisitProcessorTests(BaseProcessorTests):

    db = None    
    mood_prc = None
    stats_mgr = None
    logger = None

    def setUp(self):
        self.db = self.get_conn().test_personal_stats_medical_visit
        self.get_conn().drop_database("test_personal_stats_medical_visit")
        
        logger = self.get_logger()
        
        mgr_locator = self.get_mgr_locator(self.db)
        self.stats_mgr = mgr_locator.stats_mgr
        #Ver managers y sus conexiones.
        self.meta_mgr = mgr_locator.meta_mgr
        self.report_mgr = mgr_locator.reports_mgr
        
        self.proccesor = MedicalVisitProcessor(logger, mgr_locator)

    def tearDown(self):
        self.get_conn().drop_database("test_personal_stats_medical_visit")

    def test_accept_valid_log(self):
        log = self._get_valid_log()
        assert self.proccesor.accept(log) == True

    def test_accept_invalid_log(self):
        log = self._get_invalid_log()
        assert self.proccesor.accept(log) == False

    def test_insert(self):
        valid_log = self._get_valid_log()
        
        user_id = "DG3NQF"
        user_date = "2011-07-15" 
        week_id = StatsUtils.get_wikilife_week_info(user_date)[0]
        self._create_test_initial_data(user_id, week_id)
        
        self.proccesor.insert(valid_log)
        stats = self.stats_mgr.get_stats(user_id, week_id)

        assert stats ==  {u'count_medical_visits': [0, 0, 1, 0, 3, 0, 0],
                                                 u'_id': u'DG3NQF-2114',
                                                  u'user_id': u'DG3NQF',
                                                   u'medical_visits': [[], [], 
                                                             [{u'where': "Clinic" ,u'node_id': 251045, u'time': u'12:12:12'}],
                                                              [], [{u'where': "Hospital", u'node_id': 251045, u'time': u'13:12:12'},
                                                                    {u'where': "Clinic", u'node_id': 251045, u'time': u'14:12:12'},
                                                                     {u'where': "Clinic", u'node_id': 251045, u'time': u'15:19:31'}],
                                                              [], []],
                                                     u'week_id': 2114}
        
        report = self.report_mgr.get_medical_visits_reports("DG3NQF", "2011-07-15", "2011-07-15", 1)[0]
        #print report
        assert report == {u'user_id': u'DG3NQF', 
                                    u'log_id': 36, 
                                    u'where': "Clinic", 
                                    u'node_id': 251045, 
                                    u'time': u'15:19:31',
                                     u'date': u'2011-07-15', 
                                     u'_id': u'DG3NQF-251045-36'}

    def test_delete(self):
        valid_log = self._get_delete_log()
        
        user_id = "DG3NQF"
        user_date = "2011-07-15" #friday
        week_id, day_index = StatsUtils.get_wikilife_week_info(user_date)

        self._create_test_initial_data(user_id, week_id)
        
        #try:
        self.proccesor.delete(valid_log)
        stats = self.proccesor._get_stats(self.stats_mgr, user_id, week_id)
        #print stats
        assert stats ==  {u'user_id': u'DG3NQF', 
                                    u'_id': u'DG3NQF-2114', 
                                    u'count_medical_visits': [0, 0, 1, 0, 1, 0, 0], 
                                    u'medical_visits': [[], [], 
                                              [{u'where': "Clinic", u'node_id': 251045, u'time': u'12:12:12'}], 
                                              [], [{u'where': "Clinic", u'node_id': 251045, u'time': u'14:12:12'}], 
                                              [], []], 
                                    u'week_id': 2114}
        
        report = list(self.report_mgr.get_medical_visits_reports("DG3NQF", "2011-07-15", "2011-07-15", 1))
        assert report == []

            
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
                                 u'nodes': [{u'node_namespace': u'wikilife.healthcare.medical-record.medical-visit.infectologist-visit.where.value-node', u'node_id': 251047, u'value': "Clinic"}], u'user_log': 1}}
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
                                 u'nodes': [{u'node_namespace': u'wikilife.healthcare.medical-record.medical-visit.infectologist-visit.where.value-node', u'node_id': 251047, u'value': "Hospital"}], u'user_log': 1}}
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
    
    def _create_test_initial_data(self, user_id, week_id):

        stats = self.stats_mgr.create_stats(user_id, week_id)
        info_1 = {}
        info_1["node_id"] = 251045
        info_1["where"] = "Clinic"
        info_1["time"] = "12:12:12"
        
        info_2 = {}
        info_2["node_id"] = 251045
        info_2["where"] = "Hospital"
        info_2["time"] = "13:12:12"
        
        info_3 = {}
        info_3["node_id"] = 251045
        info_3["where"] = "Clinic"
        info_3["time"] = "14:12:12"
        
        stats["medical_visits"] = [[], [], [info_1], [], [info_2,info_3], [], []]
        stats["count_medical_visits"] = [0, 0, 1, 0, 2, 0, 0]
        
        self.stats_mgr.save_stats(stats)
        
        
        