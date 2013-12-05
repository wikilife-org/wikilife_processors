# coding=utf-8
from wikilife_processors.tests.base_test import BaseTest
from wikilife_utils.date_utils import DateUtils

class ProcessorControllerTests(BaseTest):
    
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_minimal(self):
        prc_ctrl = self.get_service_builder().build_processor_controller()
        raw_log = self._get_test_raw_log()
        self.publish_log(raw_log)
        prc_ctrl.start()
        
    """ helpers """ 
    
    def _get_test_raw_log(self):
        return {
            "test": True,
            "oper" : "i",
            "create_datetime_utc" : DateUtils.get_datetime_utc(),
            "fields" : {
                "status" : 1,
                "source" : "crawler.twitter.nikeplus",
                "original_entry" : 0,
                "root_slug" : "exercise",
                "user_id" : "A93TUV",
                "text" : "Running Distance 8.43 km",
                "nodes" : [
                    {
                        "node_namespace" : "wikilife.exercise.exercise.running.distance.value-node",
                        "node_id" : 241561,
                        "value" : 8.43
                    }
                ],
                "execute_time" : "2012-06-02 16:33:13 +0000"
            },
            "pk" : 595691,
            "model" : "LogEntry"
        }