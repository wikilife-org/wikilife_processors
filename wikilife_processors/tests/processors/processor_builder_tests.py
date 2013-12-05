# coding=utf-8
from wikilife_processors.tests.base_test import BaseTest
from wikilife_processors.manager_locator import Managers
from wikilife_processors.processors.processor_builder import ProcessorBuilder
from wikilife_processors.processors.stats.sleep_processor import SleepProcessor

class ProcessorBuilderTests(BaseTest):
    
    def setUp(self):
        mgr_locator = Managers(None, None)
        self.processor_builder = ProcessorBuilder(self.get_logger(), mgr_locator)
    
    def tearDown(self):
        pass
    
    def test_build_sleep_processor(self):
        processor_class_fullname = "wikilife_processors.processors.stats.sleep_processor.SleepProcessor"

        try:
            processor = self.processor_builder.build_processor(processor_class_fullname)    
            assert processor != None
            assert isinstance(processor, SleepProcessor) == True
             
        except Exception, e:
            print e
            assert False
        