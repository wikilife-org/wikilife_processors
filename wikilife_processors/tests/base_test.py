# coding=utf-8

from wikilife_data.utils.dao_builder import DAOBuilder
from wikilife_data.utils.db_conn import DBConn
from wikilife_processors.utils.service_builder import ServiceBuilder
from wikilife_utils.queue_publisher import QueuePublisher
from wikilife_utils.settings.settings_loader import SettingsLoader
import time
import unittest


class BaseTest(unittest.TestCase):

    _settings = None

    def get_settings(self):
        if not self._settings:
            self._settings = SettingsLoader().load_settings("tests")
        return self._settings

    def get_logger(self):
        return MockLogger() 

    def get_db_conn(self):
        db_user = None
        db_pass = None
        return DBConn(self.get_settings()["DB_SETTINGS"], db_user, db_pass)

    def get_dao_builder(self):
        return DAOBuilder(self.get_logger(), self.get_db_conn())

    def get_prc_builder(self):
        return self.get_service_builder()._build_processor_builder()

    def get_service_builder(self):
        return ServiceBuilder(self.get_settings(), self.get_logger(), self.get_dao_builder())

    def publish_log(self, raw_log):
        logs_queue_publisher = QueuePublisher(self.get_settings()["QUEUE_LOGS"])
        logs_queue_publisher.open_conn()
        logs_queue_publisher.publish(raw_log)

    def create_final_log(self, log_id=1, oper="i", user_id="QWERTY", text="test log text", category="test_categ", source="prc.test", location="Test Location", log_nodes=[], create_datetime_utc=None, execute_datetime=None, update_datetime=None, start=None, end=None):
        final_log =  {
            "_id": log_id,
            "oper": oper,
            "create_datetime_utc": create_datetime_utc,
            "user_id": user_id,
            "text": text,
            "category": category,
            "execute_datetime": execute_datetime,
            "update_datetime": update_datetime,
            "start": start,
            "end": end,
            "source": source,
            "location": location,
            "nodes": log_nodes
        }
        
        try:
            ancestors = self.get_service_builder()._build_ancestors()
            ancestors.add_ancestors_to_final_log(final_log)
        except Exception, e:
            print "Warning %s" %e
            
        return final_log

    def wait_seconds(self, seconds, msg=""):
        print "sleeping %s sec %s..." % (seconds, msg)
        time.sleep(seconds)


class MockLogger(object):

    def info(self, message):
        print message

    def error(self, message):
        print message
