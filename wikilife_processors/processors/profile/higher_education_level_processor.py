# coding=utf-8
from wikilife_processors.processors.user_option_last_log_processor import UserOptionLastLogProcessor


class HigherEducationLevelProcessor(UserOptionLastLogProcessor):
    
    def _initialize(self):
        self._lv = {"nodeId": 0, "metricId":0}
        self._dao = self._daos.user_option_last_log_dao.get_instance_for_life_variable_ns("higher_education_level")
