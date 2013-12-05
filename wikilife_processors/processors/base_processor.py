# coding=utf-8

from abc import abstractmethod
from wikilife_data.dao.processors.final_log_dao import CREATE_UTC_FIELD
from wikilife_data.dao.processors.processor_status_dao import SINCE_UTC_FIELD
from wikilife_utils.date_utils import DateUtils
import sys
import time
import traceback

OPER_INSERT = "i"
OPER_UPDATE = "u"
OPER_DELETE = "d"


class BaseProcessorException(Exception):
    pass


class BaseProcessor(object):
    """
    Abstract class
    """

    _prc_id = None
    _logger = None
    _daos = None
    _ancestors = None

    def __init__(self, prc_id, logger, daos, ancestors):
        self._prc_id = prc_id
        self._logger = logger
        self._daos = daos
        self._ancestors = ancestors
        self._initialize()

    #TODO name confusing with public initialize()
    def _initialize(self):
        pass

    def accept(self, final_log):
        """
        Returns tupple (Boolean, accepted log_nodes list)
        """

        accepted_log_nodes = []

        try:
            for log_node in final_log["nodes"]:
                if self._is_valid_log_node(log_node):
                    accepted_log_nodes.append(log_node)

        except Exception, e:
            self._logger.error(e)

        return len(accepted_log_nodes) > 0, accepted_log_nodes

    @abstractmethod
    def _is_valid_log_node(self, log_node):
        raise BaseProcessorException("Unimplemented abstract method")

    @abstractmethod
    def insert(self, final_log, log_nodes):
        """
        final_log:  Accepted final log to be inserted
        log_nodes:  Accepted log nodes, may be less than final_log log_nodes
        """
        raise BaseProcessorException("Unimplemented abstract method")

    @abstractmethod
    def delete(self, old_final_log, old_log_nodes):
        """
        old_final_log:  Accepted final log to be deleted
        old_log_nodes:  Accepted log nodes, may be less than old_final_log log_nodes
        """
        raise BaseProcessorException("Unimplemented abstract method")

    def update(self, final_log, log_nodes, old_final_log, old_log_nodes):
        """
        final_log:  Accepted final log to be inserted
        log_nodes:  Accepted log nodes, may be less than final_log log_nodes
        old_final_log:  Accepted final log to be deleted
        old_log_nodes:  Accepted log nodes, may be less than old_final_log log_nodes
        """
        self.delete(old_final_log, old_log_nodes)
        self.insert(final_log, log_nodes)

    '''
    def execute(self, oper, final_log, old_final_log):
        """
        oper: See constants
        log: Current final log  for INSERT and UPDATE opers
        old_log: Old final log, for UPDATE and DELETE opers
        """

        if oper == OPER_INSERT:
            if self.accept(final_log):
                self.insert(final_log)

        elif oper == OPER_UPDATE:
            if self.accept(final_log):
                self.update(final_log, old_final_log)

        elif oper == OPER_DELETE:
            if self.accept(old_final_log):
                self.delete(old_final_log)

        else:
            raise BaseProcessorException("unknown log operation code %s" %oper) 
    '''
    def execute(self, oper, final_log, old_final_log):
        """
        oper: See constants
        log: Current final log  for INSERT and UPDATE opers
        old_log: Old final log, for UPDATE and DELETE opers
        """

        if oper == OPER_INSERT:
            accepted, log_nodes = self.accept(final_log) 
            if accepted:
                self.insert(final_log, log_nodes)

        elif oper == OPER_UPDATE:
            accepted, log_nodes = self.accept(final_log) 
            accepted, old_log_nodes = self.accept(old_final_log) 
            if accepted:
                self.update(final_log, log_nodes, old_final_log, old_log_nodes)

        elif oper == OPER_DELETE:
            accepted, old_log_nodes = self.accept(old_final_log) 
            if accepted:
                self.delete(old_final_log, old_log_nodes)

        else:
            raise BaseProcessorException("unknown log operation code %s" %oper) 

    """ Initialization related methods """

    def initialize(self, days_offset):
        """
        days_offset: Integer. Days before processor since date.
        """
        prc_status_mo = self._validate_status()
        date_to = prc_status_mo[SINCE_UTC_FIELD]
        date_from = DateUtils.add_days(date_to, -days_offset)
        print "from %s" %date_from
        print "to %s ..." %date_to
        final_logs_cursor = self._daos.final_log_dao.get_final_logs_by_create_datetime_utc_range_desc(date_from, date_to)
        self._process_logs(final_logs_cursor, prc_status_mo)

    def _validate_status(self):
        prc_status_mo = self._daos.processor_status_dao.get_processor_status(self._prc_id)

        if prc_status_mo == None:
            raise BaseProcessor("ERROR: Processor is not registered. Must be running to be initilized.")

        return prc_status_mo 

    def _process_logs(self, final_logs_cursor, prc_status_mo):

        final_logs_count = final_logs_cursor.count()

        if final_logs_count == 0:
            raise BaseProcessorException("ERROR: No pending logs.")

        print "%s Processing %s logs" %(self._prc_id, final_logs_count)

        start_time = time.time()

        for final_log in final_logs_cursor:
            try:
                self._ancestors.add_ancestors_to_final_log(final_log)
                accepted, log_nodes = self.accept(final_log) 
                if accepted:
                    self.insert(final_log, log_nodes)

            except Exception, e:
                exc_traceback = sys.exc_info()[2]
                self._logger.error("## %s, raw_log: %s" %(traceback.print_tb(exc_traceback), final_log))

            finally:
                prc_status_mo[SINCE_UTC_FIELD] = final_log[CREATE_UTC_FIELD]
                self._daos.processor_status_dao.update_processor_status(prc_status_mo)

        print "\nSUCCESS elapsed time: %s seconds \n" %(time.time()-start_time)
