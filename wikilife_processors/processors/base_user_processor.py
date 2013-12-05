# coding=utf-8

from abc import abstractmethod
from wikilife_processors.processors.base_processor import BaseProcessor


class BaseUserProcessorException(Exception):
    pass


class BaseUserProcessor(BaseProcessor):
    """
    Abstract class
    """

    """ Initialization related methods """

    #TODO days_offset
    def initialize_by_user(self, user_id, days_offset=None):
        """
        user_id: Internal user id
        """
        prc_status_mo = self._validate_status()
        final_logs_cursor = self._daos.final_log_dao.get_final_logs_by_user(user_id)
        print "user_id %s" %user_id
        self._process_logs(final_logs_cursor, prc_status_mo)

    @abstractmethod
    def remove_by_user(self, user_id):
        raise BaseUserProcessorException("Unimplemented abstract method")
