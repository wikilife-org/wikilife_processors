# coding=utf-8

from wikilife_processors.cronned_processors.base_cronned_processor import BaseCronnedProcessor


class ProfileAgregator(BaseCronnedProcessor):

    def process(self):
        """
        get last exec
        exec report (update mapreduce collections)
        update last exec 
        """
        
        self._mgrs.profile_report_mgr.execute_full_profile_report(self.get_last_exec_utc())
