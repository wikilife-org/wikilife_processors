# coding=utf-8

from wikilife_processors.tests.base_test import BaseTest
from wikilife_utils.stats_utils import StatsUtils

class GenericProcessorTests(BaseTest):

    def setUp(self):
        
        self.get_conn().drop_database("test_generic_processor")
        self.db = self.get_conn().test_generic_processor
        
    def tearDown(self):
        self.get_conn().drop_database("test_generic_processor")

    def test_accept(self):
        pass
        
    def test_process(self):
        pass

