# coding=utf-8

from wikilife_utils.date_utils import DateUtils
import datetime
from wikilife_data.dao.processors.processor_status_dao import SINCE_UTC_FIELD
from wikilife_data.dao.processors.final_log_processor_status_dao import STARTED_UTC_FIELD,LAST_INITIALIZED_RAW_LOG_UTC_FIELD
from wikilife_data.dao.processors.final_log_dao import CREATE_UTC_FIELD as FL_CREATE_UTC_FIELD


class ProcessorInfoException(Exception):
    pass

class ProcessorInfo(object):
    """
    """
    _logger = None
    _flprc_class_fullname = None
    _log_dao = None
    _final_log_dao = None
    _prc_status_dao = None
    _flprc_status_dao = None
    
    def __init__(self, logger, flprc_class_fullname, log_dao, final_log_dao, prc_status_dao, flprc_status_dao):
        self._logger = logger
        self._flprc_class_fullname = flprc_class_fullname  
        self._log_dao = log_dao
        self._final_log_dao = final_log_dao
        self._prc_status_dao = prc_status_dao
        self._flprc_status_dao = flprc_status_dao

    def print_processor_list(self):
        print "Registered/running processors:"
        print "=============================="

        prc_cursor = self._prc_status_dao.get_processors_status()
        print "Total: %s" %prc_cursor.count()

        for prc in prc_cursor:
            print "%s" %prc["_id"]
            print "Logs processed since: %s\n" %prc[SINCE_UTC_FIELD]

    def print_processor_status(self, prc_id):
        """
        prc_id: String. processor_class_fullname
        """
        print "%s" %prc_id
        print "========================================================================="

        prc_status_mo = self._prc_status_dao.get_processor_status(prc_id)

        if prc_status_mo != None:
            total_logs = self._final_log_dao.get_final_logs_count()

            if total_logs > 0:
                first_log = self._final_log_dao.get_first_final_log()
                date_from = first_log[FL_CREATE_UTC_FIELD]
                date_to = prc_status_mo[SINCE_UTC_FIELD]
                raw_logs_cursor = self._final_log_dao.get_final_logs_by_create_datetime_utc_range_desc(date_from, date_to)
                pending_logs_count = raw_logs_cursor.count()

                print "Processed since: %s" %date_to
                print "Pending final logs: %s" %pending_logs_count
                print "DB final logs first: %s" %date_from
                print "DB final logs total: %s" %total_logs

            else:
                print "WARNING: No final logs found"
        else:
            print "ERROR: Processor not found"

    def print_final_log_processor_status(self):
        print "Final log processor id: %s" %self._flprc_class_fullname
        print "================================================================================="

        status_mo = self._flprc_status_dao.get_status()
        
        if status_mo != None:
            print "Started ......... : %s" %status_mo[STARTED_UTC_FIELD]
            print "Last init raw log : %s" %status_mo[LAST_INITIALIZED_RAW_LOG_UTC_FIELD]
            print "First raw log ... : %s" %self._log_dao.get_first_log()[FL_CREATE_UTC_FIELD]

            date_from = status_mo[LAST_INITIALIZED_RAW_LOG_UTC_FIELD]
            date_to = status_mo[STARTED_UTC_FIELD]
            pending_raw_logs_cursor = self._log_dao.get_logs_by_create_datetime_utc_range_asc(date_from, date_to)
            print "Total raw logs .. : %s" %self._log_dao.get_logs_count()
            print "Pending raw logs  : %s" %pending_raw_logs_cursor.count()

        else:
            print "ERROR: Final Log Processor status not found"

    def print_final_logs_by_month(self):
        print "Final logs by Month:"
        print "==================="

        total_logs = self._final_log_dao.get_final_logs_count()

        if total_logs > 0: 
            first_log = self._final_log_dao.get_first_final_log()
            date_from = first_log[FL_CREATE_UTC_FIELD]
            date_from = datetime.datetime(date_from.year, date_from.month, 1)
            date_to = DateUtils.add_months(date_from, 1)
            date_now = DateUtils.get_datetime_utc()

            print "DB final logs first: %s" %first_log[FL_CREATE_UTC_FIELD]
            print "DB final logs total: %s" %total_logs
            print "---------------------------------------------"

            months = []

            while date_from <= date_now:
                cursor = self._final_log_dao.get_final_logs_by_create_datetime_utc_range_desc(date_from, date_to)
                months.append((date_from, cursor.count()))
                date_from = DateUtils.add_months(date_from, 1)
                date_to = DateUtils.add_months(date_to, 1)

            for month in months:
                d, count = month
                print "%s-%02d: %s" %(d.year, d.month, count)

        else:
            print "No final logs found"
