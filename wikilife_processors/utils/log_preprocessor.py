# coding=utf-8

from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_utils.parsers.date_parser import DateParser

class LogPreprocessor(object):

    _meta_dao = None
    _vn_ancestors_map = {}

    def __init__(self, meta_dao):
        self._meta_dao = meta_dao

    def preprocess_raw_log(self, raw_log):
        if not "update" in raw_log:
            raw_log["update"] = self._create_update_time_from_execute_time(DateParser.from_datetime(raw_log["start"]), raw_log["createUTC"])

        """
        for node in raw_log["nodes"]:
            node["ancestors"] = self._get_ancestors(node["nodeId"])

            #assumes that at least should be root->categ->loggable->prop->vn
            if len(node["ancestors"]) > 3:
                node["loggableId"] = node["ancestors"][1]
                node["propertyId"] = node["ancestors"][0] 
                node["propertySlug"] = self._meta_dao.get_node_by_id(node["propertyId"])["fields"]["slug"]

            else:
                node["loggableId"] = 0
                node["propertyId"] = 0
                node["propertySlug"] = ""
        """

    def _create_update_time_from_execute_time(self, start, create_time_utc):
        update_datetime = create_time_utc.replace(tzinfo = start.tzinfo)
        return DateFormatter.to_datetime(update_datetime).replace("UTC", "+0000")

    """
    def _get_ancestors(self, value_node_id):
        if not value_node_id in self._vn_ancestors_map:
            self._vn_ancestors_map[value_node_id] = self._meta_dao.get_ancestors_ids(value_node_id)

        return self._vn_ancestors_map[value_node_id]
    """
