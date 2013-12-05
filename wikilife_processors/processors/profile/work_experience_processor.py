# coding=utf-8

from wikilife_processors.processors.base_user_processor import BaseUserProcessor
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.parsers.date_parser import DateParser


PROFILE_BIRTHDATE_KEY = "Birthdate"
LV = {"nodeId": 0, "metricId": 0}


class WorkExperienceProcessor(BaseUserProcessor):

    _dao = None
    
    def _initialize(self):
        self._dao = self._daos.generic_dao.get_instance_for(name="work_experience", indexes=[{"field": "userId", "unique": True}])

    def _is_valid_log_node(self, log_node):
        return log_node["nodeId"]==LV["nodeId"] and log_node["metricId"]==LV["metricId"]

    def insert(self, final_log, log_nodes):
        user_id = final_log["userId"]
        date_utc = DateUtils.to_datetime_utc(final_log["start"])
        profile = self._daos.profile_dao.get_profile_by_user_id(user_id)
        birthdate = DateParser.from_datetime(profile["items"][PROFILE_BIRTHDATE_KEY])
        age = (DateUtils.get_datetime_utc() - DateUtils.to_datetime_utc(birthdate)).years 

        for log_node in log_nodes:
            item = self._dao.get_single({"userId": user_id})

            if item!=None:
                if item["dateUTC"]<=date_utc:
                    item["age"] = age
                    item["experience"] = log_node["value"]
                    item["dateUTC"] = date_utc
                    self._dao.update(item)
                else:
                    self._logger.info("Attempt to log old value")
            else:
                item = {}
                item["userId"] = user_id
                item["age"] = age
                item["experience"] = log_node["value"]
                item["dateUTC"] = date_utc
                self._dao.insert(item)
