# coding=utf-8

from wikilife_processors.processors.base_user_processor import BaseUserProcessor
from wikilife_utils.date_utils import DateUtils


class ProfileProcessorException(Exception):
    pass


class ProfileProcessor(BaseUserProcessor):

    _profile_node_ids = None
    
    def _initialize(self):
        self._node_metric_id_map = {}
        items = self._daos.profile_dao.get_profile_items()
        for k in items:
            item = items[k]
            self._node_metric_id_map[item["nodeId"]] = item["metricId"] 

    def _is_valid_log_node(self, log_node):
        return log_node["nodeId"] in self._node_metric_id_map and self._node_metric_id_map[log_node["nodeId"]]==log_node["metricId"]

    def insert(self, final_log, log_nodes):
        self.update(final_log, None, None, None)

    def update(self, final_log, log_nodes, old_final_log, old_log_nodes):
        user_id = final_log["userId"]
        profile = self._daos.profile_dao.get_profile_by_user_id(user_id)

        if profile == None:
            profile = self._daos.profile_dao.get_new_profile(user_id, DateUtils.get_datetime_utc())

        for log_node in final_log["nodes"]:
            for k in profile["items"]:
                if log_node["nodeId"] == profile["items"][k]["nodeId"]:
                    profile["items"][k]["value"] = log_node["value"]
                    break #God forgive us

        self._daos.profile_dao.save_profile(profile)

    def delete(self, old_log, old_log_nodes):
        raise ProfileProcessorException("Profile log delete not allowed")
