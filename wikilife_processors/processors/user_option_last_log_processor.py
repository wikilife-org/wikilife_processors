# coding=utf-8

from wikilife_processors.processors.base_user_processor import BaseUserProcessor
from wikilife_utils.date_utils import DateUtils


class UserOptionLastLogProcessor(BaseUserProcessor):

    _lv = None
    _dao = None

    def _is_valid_log_node(self, log_node):
        return log_node["nodeId"]==self._lv["nodeId"] and log_node["metricId"]==self._lv["metricId"]

    def insert(self, final_log, log_nodes):
        user_id = final_log["userId"]
        exec_utc = DateUtils.to_datetime_utc(final_log["start"])
        
        #Should always be a single log_node 
        for log_node in log_nodes:
            user_option = self._dao.get_option_by_user_id(user_id)
            
            if user_option!=None:
                if user_option["execUTC"]<=exec_utc:
                    self._dao.update_option(user_id, log_node["value"], exec_utc)
                else:
                    self._logger.info("Attempt to log old value")
            else:
                self._dao.insert_option(user_id, log_node["value"], exec_utc)
