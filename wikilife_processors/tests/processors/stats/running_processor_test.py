# coding=utf-8
import datetime

from wikilife_processors.tests.processors.base_processor_tests import BaseProcessorTests

from wikilife_processors.processors.stats.running_processor import RunningProcessor


class RunningProcessorTests(BaseProcessorTests):

    db = None    
    stats_mgr = None
    logger = None

    def setUp(self):
        self.db = self.get_conn().test_daily_stats_running
        self.get_conn().drop_database("test_daily_stats_running")
        
        logger = self.get_logger()
        
        mgr_locator = self.get_mgr_locator(self.db)
        self.daily_stats_mgr = mgr_locator.daily_stats_mgr
        self.meta_mgr = mgr_locator.meta_mgr
        
        self.proccesor = RunningProcessor(logger, mgr_locator)

    def tearDown(self):
        self.get_conn().drop_database("test_daily_stats_running")

    def test_accept_valid_log(self):
        log = self._get_valid_log()
        assert self.proccesor.accept(log) == True

    def test_accept_invalid_log(self):
        log = self._get_invalid_log()
        assert self.proccesor.accept(log) == False

    def test_insert(self):
        valid_log = self._get_valid_log()
        
        date = "2011-10-19"
        user_id = "JMWYQG"
        timeframe = "EVENING"
        dura_value = 26.5
        dist_value = 4.4
        count = 1
        
        self.proccesor.insert(valid_log)
        stats = self.daily_stats_mgr.get_running_velocity_daily_stat(date, date, user_id, timeframe)[0]

        assert  stats["date"] == date
        assert  stats["user_id"] == user_id
        assert  stats["distance"] == dist_value
        assert  stats["duration"] == dura_value
        assert  stats["time_of_day"] == timeframe
        assert  stats["count_log"] == 1
        assert  stats["dis_avg"] == stats["distance"]
        assert  stats["dur_avg"] == stats["duration"]

        
    def _test_delete(self):
        del_log = self._get_delete_log()
        valid_log = self._get_valid_log()
        self.proccesor.insert(valid_log)
        self.processor.insert(del_log)
        self.proccesor.delete(del_log)

        date = "2011-10-19"
        user_id = "JMWYQG"
        timeframe = "EVENING"
        dura_value = 26.5
        dist_value = 4.4
        count = 1
        stats = self.daily_stats_mgr.get_running_velocity_daily_stat(date, date, user_id, timeframe)
        assert  stats["date"] == date
        assert  stats["user_id"] == user_id
        assert  stats["distance"] == dist_value
        assert  stats["duration"] == dura_value
        assert  stats["time_of_day"] == timeframe
        assert  stats["count_log"] == 1
        assert  stats["dis_avg"] == stats["distance"]
        assert  stats["dur_avg"] == stats["duration"]

    """ helpers """

    def _get_valid_log(self):
        log =  {
        "fields" : {
                "status" : 1,
                "execute_time_utc" : "Wed Oct 19 2011 17:30:03 GMT-0300 (ART)",
                "update_time" : "2011-10-19 23:30:03 +0000",
                "user_id" : "JMWYQG",
                "update_date" : "2011-10-19",
                "text" : "Running Duration 26.5 minutes Distance 4.00726656 km",
                "create_time_utc" : "Wed Oct 19 2011 19:30:03 GMT-0300 (ART)",
                "execute_date" : "2011-10-19",
                "server_id" : 42360,
                "execute_time" : "2011-10-19 19:30:03 +0000",
                "source" : "crawler.twitter.nikeplus",
                "original_entry" : 42360,
                "root_slug" : "exercise",
                "create_time" : "2011-10-19 23:30:03 +0000",
                "client_id" : 0,
                "create_date" : "2011-10-19",
                "nodes" : [
                        {
                                "node" : {
                                        "$ref" : "meta",
                                        "$id" : 298
                                },
                                "title" : "Running",
                                "node_namespace" : "wikilife.exercise.exercise.running.duration.value-node",
                                "value" : 26.5,
                                "node_id" : 298
                        },
                        {
                                "node" : {
                                        "$ref" : "meta",
                                        "$id" : 241561
                                },
                                "title" : "Running",
                                "node_namespace" : "wikilife.exercise.exercise.running.distance.value-node",
                                "value" : 4.4,
                                "node_id" : 241561
                        }
                ],
                "user_log" : 1
        },
        "model" : "LogEntry",
        "pk" : 42360
}
        return log
    
    def _get_delete_log(self):
        log =  {
        "fields" : {
                "status" : 1,
                "execute_time_utc" : "Wed Oct 19 2011 17:30:27 GMT-0300 (ART)",
                "update_time" : "2011-10-19 23:30:27 +0000",
                "user_id" : "JMWYQG",
                "update_date" : "2011-10-19",
                "text" : "Running Duration 23.4 minutes Distance 3.95898624 km",
                "create_time_utc" : "Wed Oct 05 2011 20:30:27 GMT-0300 (ART)",
                "execute_date" : "2011-10-19",
                "server_id" : 6827,
                "execute_time" : "2011-10-19 20:30:27 +0000",
                "source" : "crawler.twitter.nikeplus",
                "original_entry" : 6827,
                "root_slug" : "exercise",
                "create_time" : "2011-10-19 23:30:27 +0000",
                "client_id" : 0,
                "create_date" : "2011-10-19",
                "nodes" : [
                        {
                                "node" : {
                                        "$ref" : "meta",
                                        "$id" : 298
                                },
                                "title" : "Running",
                                "node_namespace" : "wikilife.exercise.exercise.running.duration.value-node",
                                "value" : 23.4,
                                "node_id" : 298
                        },
                        {
                                "node" : {
                                        "$ref" : "meta",
                                        "$id" : 241561
                                },
                                "title" : "Running",
                                "node_namespace" : "wikilife.exercise.exercise.running.distance.value-node",
                                "value" : 3.9,
                                "node_id" : 241561
                        }
                ],
                "user_log" : 1
        },
        "model" : "LogEntry",
        "pk" : 6827
}
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
                                u'root_slug': u'psychological', 
                                 u'nodes': [{u'node_namespace': u'wikilife.mood.mood-list.happy.intensity.value-node', u'node_id': 251339, u'value': 3}], u'user_log': 1}}
        return log
    
