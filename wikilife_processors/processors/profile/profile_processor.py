# coding=utf-8

from wikilife_processors.processors.base_user_processor import BaseUserProcessor
from wikilife_utils.date_utils import DateUtils


class ProfileProcessorException(Exception):
    pass


class ProfileProcessor(BaseUserProcessor):

    _profile_node_map = None
    
    def _initialize(self):
        self._profile_node_map = {}
        items = self._daos.profile_dao.get_profile_items()

        for k in items:
            item = items[k]
            self._profile_node_map[int(item["nodeId"])] = {"name": k, "metric_id": int(item["metricId"])} 

    def _is_valid_log_node(self, log_node):
        log_node_id = int(log_node["nodeId"]) 
        return log_node_id in self._profile_node_map and self._profile_node_map[log_node_id]["metric_id"]==log_node["metricId"]

    def insert(self, final_log, log_nodes):
        self.update(final_log, None, None, None)

    def update(self, final_log, log_nodes, old_final_log, old_log_nodes):
        user_id = final_log["userId"]
        profile = self._daos.profile_dao.get_profile_by_user_id(user_id)

        try:
            start_utc = DateUtils.to_datetime_utc(final_log["start"])
        except:
            start_utc = final_log["start"]

        updated = False

        if profile == None:
            profile = self._daos.profile_dao.get_blank_profile(user_id)

        for log_node in final_log["nodes"]:
            log_node_id = int(log_node["nodeId"]) 
            key = self._profile_node_map[log_node_id]["name"]
            item = profile["items"][key]

            if item["updateUTC"]==None or start_utc > item["updateUTC"]:
                item["value"] = log_node["value"]
                item["updateUTC"] = start_utc
                updated = True

        if updated:
            self._daos.profile_dao.save_profile(profile)

    def delete(self, old_log, old_log_nodes):
        raise ProfileProcessorException("Profile log delete not allowed")
