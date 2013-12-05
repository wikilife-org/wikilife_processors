# coding=utf-8
from wikilife_processors.tests.base_test import BaseTest
from wikilife_processors.processors.base_processor import BaseProcessor,\
    BaseProcessorException

from pymongo.connection import Connection
import wikilife_processors.tests.test_settings as settings

from wikilife_data.managers.stats.stats_manager import StatsManager
from wikilife_data.managers.meta.meta_manager import MetaManager
from wikilife_data.managers.reports.reports_manager import ReportsManager
from wikilife_data.managers.logs.log_manager import LogManager
from wikilife_data.managers.stats.daily_stats_manager import DailyStatsManager

from wikilife_processors.utils.managers import Managers

class BaseProcessorTests(BaseTest):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_accept(self):

        try:
            log = {}
            base_prc = BaseProcessor(self.get_logger(), None)

            base_prc.accept(log)
            assert False
        except BaseProcessorException, e:
            assert True
        except Exception, e:
            print e
            assert False
        
    def test_insert(self):
        
        try:
            log = {}
            base_prc = BaseProcessor(self.get_logger(), None)
            
            base_prc.insert(log)
            assert False
        except BaseProcessorException, e:
            assert True
        except Exception, e:
            print e
            assert False
            
    def  test_delete(self):
        try:
            log = {}
            base_prc = BaseProcessor(self.get_logger(), None)
            
            base_prc.delete(log)
            assert False
        except BaseProcessorException, e:
            assert True
        except Exception, e:
            print e
            assert False
    
    
    def get_mgr_locator(self, db):
        logger = self.get_logger()
        
        stats_mgr = StatsManager(logger, db)
        meta_mgr = MetaManager(logger, self.get_conn().wikilife)
        reports_mgr = ReportsManager(logger, db)
        log_mgr = LogManager(logger, self.get_conn().wikilife)
        daily_stats_mgr = DailyStatsManager(logger, db)
        manager_locator = ManagersTest(stats_mgr, meta_mgr, reports_mgr, log_mgr, daily_stats_mgr)
       
        return manager_locator
    
    
class ManagersTest(object):
    
    stats_mgr = None
    meta_mgr = None
    reports_mgr = None
    log_mgr = None
    
    def __init__(self,stats_mgr,meta_mgr, reports_mgr, log_mgr, daily_stats_mgr):
        self.stats_mgr = stats_mgr
        self.meta_mgr = meta_mgr
        self.reports_mgr = reports_mgr
        self.log_mgr = log_mgr
        self.daily_stats_mgr = daily_stats_mgr

