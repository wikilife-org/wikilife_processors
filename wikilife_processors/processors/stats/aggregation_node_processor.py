# coding=utf-8

from wikilife_processors.processors.base_user_processor import BaseUserProcessor
from wikilife_utils.date_utils import DateUtils


class AggregationNodeProcessor(BaseUserProcessor):
    """
    """

    _ancestors_ids_map = None

    def _initialize(self):
        self._ancestors_ids_map = {}

    def _get_ancestors_ids(self, node_id):

        if not node_id in self._ancestors_ids_map:
            node_ids = self._daos.meta_dao.get_ancestors_ids(node_id)
            node_ids.insert(0, node_id)
            self._ancestors_ids_map[node_id] = node_ids

        return self._ancestors_ids_map[node_id]

    def accept(self, final_log):
        return True, final_log["nodes"]

    def _add(self, final_log, log_nodes, inc):
        user_id = final_log["userId"] 
        start = final_log["start"]
        date_day = DateUtils.create_datetime(start.year, start.month, start.day)

        for log_node in log_nodes:
            try:
                node_id = int(log_node["nodeId"])
                node_ids = self._get_ancestors_ids(node_id)
                self._daos.aggregation_node_dao.inc_logged_nodes_count(node_ids, user_id, date_day, inc)

            except Exception, e:
                self._logger.error(e)

    def insert(self, final_log, log_nodes):
        self._add(final_log, log_nodes, 1)

    def delete(self, old_final_log, old_log_nodes):
        self._add(old_final_log, old_log_nodes, -1)
