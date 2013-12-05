# coding=utf-8

from wikilife_processors.internal_processors.base_internal_processor import BaseInternalProcessor


class UserMergeProcessor(BaseInternalProcessor):

    def __init__(self, user_prcs):
        self._user_prcs = user_prcs

    def process(self, internal_oper):

        user_id = internal_oper["user_id"]
        old_user_id = internal_oper["old_user_id"]
        #twitter_id_hash = internal_oper["twitter_id_hash"]

        for prc in self._user_prcs:
            prc.remove_by_user(old_user_id)
            prc.remove_by_user(user_id)
            prc.initialize_by_user(user_id)
        
        print "###done"
