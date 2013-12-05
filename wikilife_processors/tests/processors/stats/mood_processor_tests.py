# coding=utf-8
import datetime

from wikilife_processors.tests.base_test import BaseTest
from wikilife_processors.tests.processors.base_processor_tests import BaseProcessorTests

from wikilife_utils.stats_utils import StatsUtils

from wikilife_processors.processors.stats.mood_processor import MoodProcessor

class MoodProcessorTests(BaseProcessorTests):

    db = None    
    mood_prc = None
    stats_mgr = None
    logger = None

    def setUp(self):
        self.db = self.get_conn().test_personal_stats_moods
        self.get_conn().drop_database("test_personal_stats_moods")
        
        logger = self.get_logger()
        
        mgr_locator = self.get_mgr_locator(self.db)
        self.stats_mgr = mgr_locator.stats_mgr
        #Ver managers y sus conexiones.
        self.meta_mgr = mgr_locator.meta_mgr
        self.report_mgr = mgr_locator.reports_mgr
        
        self.mood_prc = MoodProcessor(logger, mgr_locator)

    def tearDown(self):
        self.get_conn().drop_database("test_personal_stats_moods")

    def test_accept_valid_log(self):
        log = self._get_mood_valid_log()

        assert self.mood_prc.accept(log) == True

    def test_accept_invalid_log(self):
        log = self._get_invalid_log()

        assert self.mood_prc.accept(log) == False

    def test_insert(self):
        valid_log = self._get_mood_valid_log()
        
        user_id = "DG3NQF"
        user_date = "2011-07-15" 
        week_id = StatsUtils.get_wikilife_week_info(user_date)[0]
        self._create_test_initial_data(user_id, week_id)
        
        self.mood_prc.insert(valid_log)
        stats = self.stats_mgr.get_stats(user_id, week_id)

        assert stats ==  {u'count_mood': [0, 0, 1, 0, 3, 0, 0],
                                                 u'_id': u'DG3NQF-2114',
                                                  u'user_id': u'DG3NQF',
                                                   u'mood': [[], [], 
                                                             [{u'intensity': 8, u'node_id': 251337, u'time': u'12:12:12'}],
                                                              [], [{u'intensity': 4, u'node_id': 251337, u'time': u'13:12:12'},
                                                                    {u'intensity': 5, u'node_id': 251337, u'time': u'14:12:12'},
                                                                     {u'intensity': 3, u'node_id': 251337.0, u'time': u'15:19:31'}],
                                                              [], []],
                                                     u'week_id': 2114}
        
        report = self.report_mgr.get_moods_reports("DG3NQF", "2011-07-15", "2011-07-15", 1)[0]
        #print report
        assert report == {u'user_id': u'DG3NQF', 
                                    u'log_id': 36, 
                                    u'intensity': 3, 
                                    u'node_id': 251337.0, 
                                    u'time': u'15:19:31',
                                     u'date': u'2011-07-15', 
                                     u'_id': u'DG3NQF-251337-36'}

    def test_delete(self):
        valid_log = self._get_mood_delete_log()
        
        user_id = "DG3NQF"
        user_date = "2011-07-15" #friday
        week_id = StatsUtils.get_wikilife_week_info(user_date)[0]
        self._create_test_initial_data(user_id, week_id)
        
        #try:
        self.mood_prc.delete(valid_log)
        stats = self.mood_prc._get_stats(self.stats_mgr, user_id, week_id)
        #print stats
        assert stats ==  {u'user_id': u'DG3NQF', 
                                    u'_id': u'DG3NQF-2114', 
                                    u'count_mood': [0, 0, 1, 0, 2, 0, 0], 
                                    u'mood': [[], [], 
                                              [{u'intensity': 8, u'node_id': 251337, u'time': u'12:12:12'}], 
                                              [], [{u'intensity': 4, u'node_id': 251337, u'time': u'13:12:12'}, 
                                                   {u'intensity': 5, u'node_id': 251337, u'time': u'14:12:12'}], 
                                              [], []], 
                                    u'week_id': 2114}
        
        report = list(self.report_mgr.get_moods_reports("DG3NQF", "2011-07-15", "2011-07-15", 1))
        assert report == []

            
    """ helpers """

    def _get_mood_valid_log(self):
        log =  {u'pk': 36, 
                u'model': u'LogEntry', 
                u'fields': {u'status': 1, 
                                u'server_id': 36, 
                                u'user_id': u'DG3NQF', 
                                u'client_id': 15, 
                                u'text': u'Mood 8', 
                                u'execute_time': u'2011-07-15 15:19:31 +0000', 
                                u'original_entry': 0,
                                u'root_slug': u'psychological', 
                                 u'nodes': [{u'node_namespace': u'wikilife.psychological.mood-list.mood.intensity.value-node', u'node_id': 251339, u'value': 3}], u'user_log': 1}}
        return log
    
    def _get_mood_delete_log(self):
        log =  {u'pk': 36, 
                u'model': u'LogEntry', 
                u'fields': {u'status': 1, 
                                u'server_id': 36, 
                                u'user_id': u'DG3NQF', 
                                u'client_id': 15, 
                                u'text': u'Mood 8', 
                                u'execute_time': u'2011-07-15 15:19:31 +0000', 
                                u'original_entry': 0,
                                u'root_slug': u'psychological', 
                                 u'nodes': [{u'node_namespace': u'wikilife.mood.mood-list.mood.intensity.value-node', u'node_id': 251339, u'value': 3}], u'user_log': 1}}
        return log
    
    def _get_invalid_log(self):
        log =  {u'pk': 36, 
                u'model': u'LogEntry', 
                u'fields': {u'status': 1, 
                                u'server_id': 36, 
                                u'user_id': u'DG3NQF', 
                                u'client_id': 15, 
                                u'text': u'Mood 8', 
                                u'execute_time': u'2011-07-15 15:19:31 +0000', 
                                u'original_entry': 0,
                                u'root_slug': u'psychological', 
                                 u'nodes': [{u'node_namespace': u'wikilife.mood.mood-list.happy.intensity.value-node', u'node_id': 251339, u'value': 3}], u'user_log': 1}}
        return log
    
    def _create_test_initial_data(self, user_id, week_id):

        stats = self.stats_mgr.create_stats(user_id, week_id)
        info_1 = {}
        info_1["node_id"] = 251337
        info_1["intensity"] = 8
        info_1["time"] = "12:12:12"
        
        info_2 = {}
        info_2["node_id"] = 251337
        info_2["intensity"] = 4
        info_2["time"] = "13:12:12"
        
        info_3 = {}
        info_3["node_id"] = 251337
        info_3["intensity"] = 5
        info_3["time"] = "14:12:12"
        stats["mood"] = [[], [], [info_1], [], [info_2,info_3], [], []]
        stats["count_mood"] = [0, 0, 1, 0, 2, 0, 0]
        self.stats_mgr.save_stats(stats)
        
        
        