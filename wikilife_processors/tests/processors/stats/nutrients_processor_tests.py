# coding=utf-8
import datetime

from wikilife_processors.tests.base_test import BaseTest
from wikilife_utils.stats_utils import StatsUtils

from wikilife_processors.processors.stats.nutrients_processor import NutrientProcessor


class NutrientsProcessorTests(BaseTest):

    db = None
    nutrient_prc = None
    stats_mgr = None
    logger = None
    meta_mgr = None

    def setUp(self):
        self.db = self.get_conn().test_personal_stats_nutrient
        self.get_conn().drop_database("test_personal_stats_nutrient")
        
        logger = self.get_logger()
        
        mgr_locator = self.get_mgr_locator(self.db)
        self.stats_mgr = mgr_locator.get_stats_mgr()
        self.meta_mgr = mgr_locator.get_meta_mgr()
        
        self.nutrient_prc = NutrientProcessor(logger, mgr_locator)

    def tearDown(self):
        self.get_conn().drop_database("test_personal_stats_nutrient")

    def test_accept_valid_log(self):
        log = self._get_nutrient_valid_log()

        assert self.nutrient_prc.accept(log) == True

    def test_accept_invalid_log(self):
        log = {}

        assert self.nutrient_prc.accept(log) == False

    def test_accept_other_log(self):
        log = self._get_other_valid_log()

        assert self.nutrient_prc.accept(log) == False


    def test_process1(self):
        valid_log = self._get_nutrient_valid_log()
        
        user_id = "DG3NQF"
        user_date = "2011-07-15" #friday
        week_id = StatsUtils.get_wikilife_week_info(user_date)[0]
        self._create_test_initial_data(user_id, week_id, 1)
        
        try:
            self.nutrient_prc.process(valid_log)
            stats = self.nutrient_prc._get_stats(self.stats_mgr, user_id, week_id)
            
            print stats["sum_carbs"]
            
            assert stats["sum_carbs"] ==  [1.0, 2.0, 3.0, 4.0, 1254.0, 6.0, 7.0]
        
        except Exception, e:
            print e
            assert False

    def test_process1_delete(self):
        valid_log = self._get_nutrient_delete_log()
        
        user_id = "DG3NQF"
        user_date = "2011-07-15" #friday
        week_id = StatsUtils.get_wikilife_week_info(user_date)[0]
        self._create_test_initial_data(user_id, week_id, 1)
        
        try:
            self.nutrient_prc.process_delete(valid_log)
            stats = self.nutrient_prc._get_stats(self.stats_mgr, user_id, week_id)
            
            print stats["sum_carbs"]
            
            assert stats["sum_carbs"] ==  [1.0, 2.0, 3.0, 4.0, 746.0, 6.0, 7.0]
        
        except Exception, e:
            print e
            assert False


    def test_process2(self):
        valid_log = self._get_nutrient_valid_log()
        
        user_id = "DG3NQF"
        user_date = "2011-07-15" #friday
        week_id = StatsUtils.get_wikilife_week_info(user_date)[0]
        self._create_test_initial_data(user_id, week_id, 1)
        
        try:
            self.nutrient_prc.process(valid_log)
            stats = self.nutrient_prc._get_stats(self.stats_mgr, user_id, week_id)
            
            print stats["sum_fiber"]
            
            assert stats["sum_fiber"] ==  [1.0, 2.0, 3.0, 4.0, 1255.0, 6.0, 7.0]
        
        except Exception, e:
            print e
            assert False
          
          
    def test_process2_delete(self):
        valid_log = self._get_nutrient_delete_log()
        
        user_id = "DG3NQF"
        user_date = "2011-07-15" #friday
        week_id = StatsUtils.get_wikilife_week_info(user_date)[0]
        self._create_test_initial_data(user_id, week_id, 1)
        
        try:
            self.nutrient_prc.process_delete(valid_log)
            stats = self.nutrient_prc._get_stats(self.stats_mgr, user_id, week_id)
            
            print stats["sum_fiber"]
            
            assert stats["sum_fiber"] ==  [1.0, 2.0, 3.0, 4.0, 745.0, 6.0, 7.0]
        
        except Exception, e:
            print e
            assert False          
            
    def test_process3(self):
        valid_log = self._get_nutrient_valid_log()
        
        user_id = "DG3NQF"
        user_date = "2011-07-15" #friday
        week_id = StatsUtils.get_wikilife_week_info(user_date)[0]
        self._create_test_initial_data(user_id, week_id, 1)
        
        try:
            self.nutrient_prc.process(valid_log)
            stats = self.nutrient_prc._get_stats(self.stats_mgr, user_id, week_id)
            
            print stats["sum_protein"]
            
            assert stats["sum_protein"] ==  [1.0, 2.0, 3.0, 4.0, 1256.0, 6.0, 7.0]
        
        except Exception, e:
            print e
            assert False
     
    def test_process3_delete(self):
        valid_log = self._get_nutrient_delete_log()
        
        user_id = "DG3NQF"
        user_date = "2011-07-15" #friday
        week_id = StatsUtils.get_wikilife_week_info(user_date)[0]
        self._create_test_initial_data(user_id, week_id, 1)
        
        try:
            self.nutrient_prc.process_delete(valid_log)
            stats = self.nutrient_prc._get_stats(self.stats_mgr, user_id, week_id)
            
            print stats["sum_protein"]
            
            assert stats["sum_protein"] ==  [1.0, 2.0, 3.0, 4.0, 744.0, 6.0, 7.0]
        
        except Exception, e:
            print e
            assert False     
            
    def test_process4(self):
        valid_log = self._get_nutrient_valid_log()
        
        user_id = "DG3NQF"
        user_date = "2011-07-15" #friday
        week_id = StatsUtils.get_wikilife_week_info(user_date)[0]
        self._create_test_initial_data(user_id, week_id, 1)
        
        try:
            self.nutrient_prc.process(valid_log)
            stats = self.nutrient_prc._get_stats(self.stats_mgr, user_id, week_id)
            
            print stats["sum_fat"]
            
            assert stats["sum_fat"] ==  [1.0, 2.0, 3.0, 4.0, 1257.0, 6.0, 7.0]
        
        except Exception, e:
            print e
            assert False                        


    def test_process4_delete(self):
        valid_log = self._get_nutrient_delete_log()
        
        user_id = "DG3NQF"
        user_date = "2011-07-15" #friday
        week_id = StatsUtils.get_wikilife_week_info(user_date)[0]
        self._create_test_initial_data(user_id, week_id, 1)
        
        try:
            self.nutrient_prc.process_delete(valid_log)
            stats = self.nutrient_prc._get_stats(self.stats_mgr, user_id, week_id)
            
            print stats["sum_fat"]
            
            assert stats["sum_fat"] ==  [1.0, 2.0, 3.0, 4.0, 743.0, 6.0, 7.0]
        
        except Exception, e:
            print e
            assert False  


    """ helpers """

    def _get_nutrient_valid_log(self):
        return {u'pk': 33, u'model': u'LogEntry', u'fields': {u'status': 1, u'execute_time_utc': datetime.datetime(2011, 7, 15, 15, 19, 31), u'server_id': 1368, u'user_id': u'DG3NQF', u'client_id': 15, u'update_date': u'2011-07-15', u'text': u'Beef Steak 1 101g', u'create_time_utc': datetime.datetime(2011, 7, 15, 18, 10, 58, 911000), u'execute_date': u'2011-07-15', u'update_time': u'2011-07-15 18:10:58 +0000', u'execute_time': u'2011-07-15 15:19:31 +0000', u'source': u'client.iphone', u'original_entry': 0, u'create_time': u'2011-07-15 18:10:58 +0000', u'root_slug': u'nutrition', u'create_date': u'2011-07-15', u'nodes': [{u'node_namespace': u'wikilife.nutrition.meal.food.beef-steak.size.value-node', u'node_id': 1368, u'value': 1.0, u'title': u'Beef Steak'}], u'user_log': 1}}

    def _get_nutrient_delete_log(self):
        return {u'pk': 33, u'model': u'LogEntry', u'fields': {u'status': 1, u'execute_time_utc': datetime.datetime(2011, 7, 15, 15, 19, 31), u'server_id': 1368, u'user_id': u'DG3NQF', u'client_id': 15, u'update_date': u'2011-07-15', u'text': u'Beef Steak 1 101g', u'create_time_utc': datetime.datetime(2011, 7, 15, 18, 10, 58, 911000), u'execute_date': u'2011-07-15', u'update_time': u'2011-07-15 18:10:58 +0000', u'execute_time': u'2011-07-15 15:19:31 +0000', u'source': u'client.iphone', u'original_entry': 0, u'create_time': u'2011-07-15 18:10:58 +0000', u'root_slug': u'nutrition', u'create_date': u'2011-07-15', u'nodes': [{u'node_namespace': u'wikilife.nutrition.meal.food.beef-steak.size.value-node', u'node_id': 1368, u'value': 1.0, u'title': u'Beef Steak'}], u'user_log': 1}}

    def _get_other_valid_log(self):
        return {u'pk': 1, u'model': u'LogEntry', u'fields': {u'status': 1, u'execute_time_utc': datetime.datetime(2011, 7, 15, 15, 19, 31), u'server_id': 2079, u'user_id': u'DG3NQF', u'client_id': 15, u'update_date': u'2011-07-15', u'text': u'Other  8 hr', u'create_time_utc': datetime.datetime(2011, 7, 15, 18, 10, 58, 911000), u'execute_date': u'2011-07-15', u'update_time': u'2011-07-15 18:10:58 +0000', u'execute_time': u'2011-07-15 15:19:31 +0000', u'source': u'client.iphone', u'original_entry': 0, u'create_time': u'2011-07-15 18:10:58 +0000', u'root_slug': u'physiological', u'create_date': u'2011-07-15', u'nodes': [{u'node_namespace': u'wikilife.physiological.other.duration.value-node', u'node_id': 5, u'value': 8.0, u'title': u'Other'}], u'user_log': 1}}

    def _create_test_initial_data(self, user_id, week_id, start_value):

        stats = self.stats_mgr.create_stats(user_id, week_id)
       
        stats["sum_carbs"] =   [1.0, 2.0, 3.0, 4.0, 1000.0, 6.0, 7.0]
        stats["count_carbs"] = [3, 3, 3, 2, 2, 2, 1]
        stats["sum_fiber"] =   [1.0, 2.0, 3.0, 4.0, 1000.0, 6.0, 7.0]
        stats["count_fiber"] = [3, 3, 3, 2, 2, 2, 1]
        stats["sum_protein"] =   [1.0, 2.0, 3.0, 4.0, 1000.0, 6.0, 7.0]
        stats["count_protein"] = [3, 3, 3, 2, 2, 2, 1]
        stats["sum_fat"] =   [1.0, 2.0, 3.0, 4.0, 1000.0, 6.0, 7.0]
        stats["count_fat"] = [3, 3, 3, 2, 2, 2, 1]
        stats["count_nutrients"] = [3, 3, 3, 2, 2, 2, 1]        
        
        
        self.stats_mgr.save_stats(stats)

        node = {}
        node["fields"] = {}
        node["fields"]["server_id"] =  1366
        node["fields"]["namespace"] =  "wikilife.nutrition.meal.food.beef-steak"   
        nutrients1 = {"tag_name": "CHOCDF", "value": 254}
        nutrients2 = {"tag_name": "FIBTG", "value": 255}
        nutrients3 = {"tag_name": "PROCNT", "value": 256}
        nutrients4 = {"tag_name": "FAT", "value": 257}
        cholesterol = {"tag_name": "CHOLE", "value": 19}
        node["fields"]["nutrients"] = []
        node["fields"]["nutrients"].append(nutrients1)
        node["fields"]["nutrients"].append(nutrients2)
        node["fields"]["nutrients"].append(nutrients3)
        node["fields"]["nutrients"].append(nutrients4)
        node["fields"]["nutrients"].append(cholesterol) 

        
        self.meta_mgr.save_node(node)
