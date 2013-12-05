# coding=utf-8

from wikilife_data.dao.stats.aggregation_dao import TYPE_NUMERIC, TYPE_OPTIONS
from wikilife_data.model.meta import NUMERIC_METRIC_NODE
from wikilife_processors.processors.base_user_processor import BaseUserProcessor
from wikilife_utils.date_utils import DateUtils


class AggregationProcessor(BaseUserProcessor):
    """
    """

    _ancestors_ids_map = None

    def _initialize(self):
        self._ancestors_ids_map = {}

    def _get_ancestors_ids_measured_by(self, node_id, metric_id):
        key = "%s_%s" %(node_id, metric_id)

        if not key in self._ancestors_ids_map:
            node_ids = self._daos.meta_dao.get_ancestors_ids_measured_by(node_id, metric_id)
            metric = self._daos.meta_dao.get_node_by_id(metric_id)

            self._ancestors_ids_map[key] = {
                "type": TYPE_NUMERIC if metric.element_type==NUMERIC_METRIC_NODE else TYPE_OPTIONS,
                "ids": node_ids  
            }

        return self._ancestors_ids_map[key]

    def accept(self, final_log):
        return True, final_log["nodes"]

    """
    def insert(self, final_log, log_nodes):
        user_id = final_log["userId"] 
        start = final_log["start"]
        date_day = DateUtils.create_datetime(start.year, start.month, start.day)

        for log_node in log_nodes:
            try:
                node_id = log_node["nodeId"]
                metric_id = log_node["metricId"]
                value = log_node["value"]

                node_ids = self._daos.meta_dao.get_ancestors_ids_measured_by(node_id, metric_id)
                node_ids.append(node_id)
                metric = self._daos.meta_dao.get_node_by_id(metric_id)
                
                type = TYPE_NUMERIC if metric.element_type == NUMERIC_METRIC_NODE else TYPE_OPTIONS
                self._daos.aggregation_dao.add(node_ids, metric_id, user_id, date_day, value, type)

            except Exception, e:
                self._logger.error(e)
    """
    def _add(self, final_log, log_nodes, aggr_dao_method):
        user_id = final_log["userId"] 
        start = final_log["start"]
        date_day = DateUtils.create_datetime(start.year, start.month, start.day)

        for log_node in log_nodes:
            try:
                node_id = int(log_node["nodeId"])
                metric_id = int(log_node["metricId"])
                value = log_node["value"]

                ancestors = self._get_ancestors_ids_measured_by(node_id, metric_id)
                type = ancestors["type"]
                node_ids = list(ancestors["ids"])
                node_ids.append(node_id)

                aggr_dao_method(node_ids, metric_id, user_id, date_day, value, type)

            except Exception, e:
                self._logger.error(e)

    def insert(self, final_log, log_nodes):
        self._add(final_log, log_nodes, self._daos.aggregation_dao.add)

    def delete(self, old_final_log, old_log_nodes):
        self._add(old_final_log, old_log_nodes, self._daos.aggregation_dao.remove)
