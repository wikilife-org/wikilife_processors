# coding=utf-8

from abc import abstractmethod
from wikilife_data.managers.processors.cronned_processor_status_manager import LAST_EXEC_UTC_FIELD
from wikilife_utils.date_utils import DateUtils
import time


class BaseCronnedProcessorException(Exception):
    pass


class BaseCronnedProcessor(object):
    """
    Abstract class
    """

    _prc_id = None
    _logger = None
    _mgrs = None

    def __init__(self, prc_id, logger, managers):
        self._prc_id = prc_id
        self._logger = logger
        self._mgrs = managers

    def execute(self):
        start_time = time.time()
        prc_status = self._mgrs.cronned_processor_status_mgr.get_cronned_processor_status(self._prc_id)

        if prc_status != None:
            last_exec_utc = prc_status[LAST_EXEC_UTC_FIELD]

        else:
            last_exec_utc = DateUtils.get_datetime_utc()
            self._mgrs.cronned_processor_status_mgr.insert_cronned_processor_status(self._prc_id, last_exec_utc)

        self._logger.info("## %s execute start" %self._prc_id)
        self.process()
        last_exec_utc = DateUtils.get_datetime_utc()
        self._mgrs.cronned_processor_status_mgr.update_cronned_processor_status(self._prc_id, last_exec_utc)
        self._logger.info("## %s execute end. Elapsed time: %s seconds" %(self._prc_id, (time.time()-start_time) ) )

    def get_last_exec_utc(self):
        self._mgrs.cronned_processor_status_mgr.get_cronned_processor_status(self._prc_id)[LAST_EXEC_UTC_FIELD]
    
    @abstractmethod
    def process(self):
        raise BaseCronnedProcessorException("Unimplemented abstract method")
