# coding=utf-8
import datetime

from wikilife_processors.tests.base_test import BaseTest
from wikilife_utils.stats_utils import StatsUtils

from wikilife_processors.processors.stats.exercise_processor import ExerciseProcessor

class ExerciseProcessorTests(BaseTest):

    db = None
    exercise_prc = None
    stats_mgr = None
    logger = None

    def setUp(self):
        self.db = self.get_conn().test_personal_stats_exercise
        self.get_conn().drop_database("test_personal_stats_exercise")
        
        logger = self.get_logger()
        
        mgr_locator = self.get_mgr_locator(self.db)
        self.stats_mgr = mgr_locator.get_stats_mgr()
        self.meta_mgr = mgr_locator.get_meta_mgr()
        
        self.exercise_prc = ExerciseProcessor(logger, mgr_locator)

    def tearDown(self):
        self.get_conn().drop_database("test_personal_stats_exercise")

    def test_accept_valid_log(self):
        log = self._get_exercise_valid_log()

        assert self.exercise_prc.accept(log) == True

    def test_accept_invalid_log(self):
        log = {}

        assert self.exercise_prc.accept(log) == False

    def test_accept_other_log(self):
        log = self._get_other_valid_log()

        assert self.exercise_prc.accept(log) == False


    def test_process(self):
        valid_log = self._get_exercise_valid_log()
        
        user_id = "DG3NQF"
        user_date = "2011-07-15" #friday
        week_id = StatsUtils.get_wikilife_week_info(user_date)[0]
        self._create_test_initial_data(user_id, week_id, 1)
        
        try:
            self.exercise_prc.process(valid_log)
            stats = self.exercise_prc._get_stats(self.stats_mgr, user_id, week_id)
            
            assert stats["exercises"] ==  [[[u'Yoga', 5, u'12:45'], [u'Karate', 5, u'12:45'], [u'Karate', 5, u'12:45']], [[u'Running', 5, u'12:45'], [u'Karate', 5, u'12:45'], [u'Karate', 5, u'12:45']], [[u'Karate', 5, u'12:45'], [u'Karate', 5, u'12:45'], [u'Karate', 5, u'12:45']], [[u'Karate', 5, u'12:45'], [u'Karate', 5, u'12:45']], [[u'Karate', 5, u'12:45'], [u'Soccer', 5, u'12:45'], [u'Yoga', 10, '15:19']], [[u'Running', 5, u'12:45'], [u'Soccer', 5, u'12:45']], [[u'Soccer', 5, u'12:45']]]
            
        except Exception, e:
            print e
            assert False


    def test_process_delete(self):
        valid_log = self._get_exercise_delete_log()
        
        user_id = "DG3NQF"
        user_date = "2011-07-15" #friday
        week_id = StatsUtils.get_wikilife_week_info(user_date)[0]
        self._create_test_initial_data(user_id, week_id, 1)
        
        try:
            self.exercise_prc.process_delete(valid_log)
            stats = self.exercise_prc._get_stats(self.stats_mgr, user_id, week_id)
            
            assert stats["exercises"] ==  [[[u'Yoga', 5, u'12:45'], [u'Karate', 5, u'12:45'], [u'Karate', 5, u'12:45']], [[u'Running', 5, u'12:45'], [u'Karate', 5, u'12:45'], [u'Karate', 5, u'12:45']], [[u'Karate', 5, u'12:45'], [u'Karate', 5, u'12:45'], [u'Karate', 5, u'12:45']], [[u'Karate', 5, u'12:45'], [u'Karate', 5, u'12:45']], [[u'Karate', 5, u'12:45']], [[u'Running', 5, u'12:45'], [u'Soccer', 5, u'12:45']], [[u'Soccer', 5, u'12:45']]]
            
        except Exception, e:
            print e
            assert False

    """ helpers """

    def _get_exercise_valid_log(self):
        return {u'pk': 36, u'model': u'LogEntry', u'fields': {u'status': 1, u'execute_time_utc': datetime.datetime(2011, 7, 15, 15, 19, 31), u'server_id': 36, u'user_id': u'DG3NQF', u'client_id': 15, u'update_date': u'2011-07-15', u'text': u'Yoga', u'create_time_utc': datetime.datetime(2011, 7, 15, 18, 10, 58, 911000), u'execute_date': u'2011-07-15', u'update_time': u'2011-07-15 18:10:58 +0000', u'execute_time': u'2011-07-15 15:19:31 +0000', u'source': u'client.iphone', u'original_entry': 0, u'create_time': u'2011-07-15 18:10:58 +0000', u'root_slug': u'exercise', u'create_date': u'2011-07-15', u'nodes': [{u'node_namespace': u'wikilife.exercise.exercise.yoga', u'node_id': 1090, u'value': 10, u'title': u'Yoga'}], u'user_log': 1}}

    def _get_exercise_delete_log(self):
        return {u'pk': 36, u'model': u'LogEntry', u'fields': {u'status': 1, u'execute_time_utc': datetime.datetime(2011, 7, 15, 15, 19, 31), u'server_id': 36, u'user_id': u'DG3NQF', u'client_id': 15, u'update_date': u'2011-07-15', u'text': u'Yoga', u'create_time_utc': datetime.datetime(2011, 7, 15, 18, 10, 58, 911000), u'execute_date': u'2011-07-15', u'update_time': u'2011-07-15 18:10:58 +0000', u'execute_time': u'2011-07-15 12:45:31 +0000', u'source': u'client.iphone', u'original_entry': 0, u'create_time': u'2011-07-15 18:10:58 +0000', u'root_slug': u'exercise', u'create_date': u'2011-07-15', u'nodes': [{u'node_namespace': u'wikilife.exercise.exercise.yoga', u'node_id': 1090, u'value': 5, u'title': u'Soccer'}], u'user_log': 1}}


    def _get_other_valid_log(self):
        return {u'pk': 1, u'model': u'LogEntry', u'fields': {u'status': 1, u'execute_time_utc': datetime.datetime(2011, 7, 15, 15, 19, 31), u'server_id': 2079, u'user_id': u'DG3NQF', u'client_id': 15, u'update_date': u'2011-07-15', u'text': u'Other  8 hr', u'create_time_utc': datetime.datetime(2011, 7, 15, 18, 10, 58, 911000), u'execute_date': u'2011-07-15', u'update_time': u'2011-07-15 18:10:58 +0000', u'execute_time': u'2011-07-15 15:19:31 +0000', u'source': u'client.iphone', u'original_entry': 0, u'create_time': u'2011-07-15 18:10:58 +0000', u'root_slug': u'physiological', u'create_date': u'2011-07-15', u'nodes': [{u'node_namespace': u'wikilife.physiological.other.duration.value-node', u'node_id': 5, u'value': 8.0, u'title': u'Other'}], u'user_log': 1}}

    def _create_test_initial_data(self, user_id, week_id, start_value):

        stats = self.stats_mgr.create_stats(user_id, week_id)
        stats["exercises"] = [[("Yoga",5,"12:45"),("Karate",5,"12:45"),("Karate",5,"12:45")], [("Running",5,"12:45"),("Karate",5,"12:45"),("Karate",5,"12:45")], [("Karate",5,"12:45"),("Karate",5,"12:45"),("Karate",5,"12:45")], [("Karate",5,"12:45"),("Karate",5,"12:45")], [("Karate",5,"12:45"),("Soccer",5,"12:45")], [("Running",5,"12:45"),("Soccer",5,"12:45")], [("Soccer",5,"12:45")] ]
        stats["count_exercise"] = [3, 3, 3, 2, 2, 2, 1]
        self.stats_mgr.save_stats(stats)
        
        
        
        
        
        
        

