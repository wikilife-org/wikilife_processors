# coding=utf-8

from wikilife_processors.tests.base_test import BaseTest


class AncestorsTests(BaseTest):

    def test_simple(self):
        meta_dao = self.get_dao_builder().build_live_meta_dao()
        ancestors = self.get_service_builder()._build_ancestors()

        vn_id = 1157
        vn_ancs = ancestors.get_ancestors(vn_id)
        assert len(vn_ancs) > 3

        vn = meta_dao.get_node_by_id(vn_id)
        print "\n%s (%s)" %(vn["fields"]["namespace"], vn["pk"])

        for anc_id in vn_ancs:
            anc = meta_dao.get_node_by_id(anc_id)
            print "%s (%s)" %(anc["fields"]["namespace"], anc["pk"])

        vn_id = 55
        vn_ancs = ancestors.get_ancestors(vn_id)
        assert len(vn_ancs) > 3

        vn = meta_dao.get_node_by_id(vn_id)
        print "\n%s (%s)" %(vn["fields"]["namespace"], vn["pk"])

        for anc_id in vn_ancs:
            anc = meta_dao.get_node_by_id(anc_id)
            print "%s (%s)" %(anc["fields"]["namespace"], anc["pk"])

        vn_id = 1157
        vn_ancs = ancestors.get_ancestors(vn_id)
        assert len(vn_ancs) > 3

        vn = meta_dao.get_node_by_id(vn_id)
        print "\n%s (%s)" %(vn["fields"]["namespace"], vn["pk"])

        for anc_id in vn_ancs:
            anc = meta_dao.get_node_by_id(anc_id)
            print "%s (%s)" %(anc["fields"]["namespace"], anc["pk"])
