# coding=utf-8

class Ancestors(object):

    _meta_dao = None
    _node_ancestors_map = {}

    def __init__(self, meta_dao):
        self._meta_dao = meta_dao

    def get_ancestors(self, node_id):
        if not node_id in self._node_ancestors_map:
            self._node_ancestors_map[node_id] = self._meta_dao.get_ancestors_ids(node_id)

        return self._node_ancestors_map[node_id]

    def add_ancestors_to_final_log(self, final_log):
        for node in final_log["nodes"]:
            node["ancestors"] = self.get_ancestors(int(node["nodeId"]))
