# coding=utf-8

from wikilife_data.dao.logs.log_dao import CREATE_UTC_FIELD
from wikilife_data.dao.processors.final_log_processor_status_dao import \
    LAST_INITIALIZED_RAW_LOG_UTC_FIELD
from wikilife_processors.processors.base_processor import OPER_INSERT, \
    OPER_UPDATE, OPER_DELETE
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_utils.parsers.date_parser import DateParser
import time


class FinalLogProcessorException(Exception):
    pass


class FinalLogProcessor(object):

    def __init__(self, prc_id, logger, log_dao, final_log_dao, flprc_status_dao, location_dao, log_preprocessor, ancestors):
        self._prc_id = prc_id
        self._logger = logger
        self._log_dao = log_dao
        self._final_log_dao = final_log_dao
        self._flprc_status_dao = flprc_status_dao
        self._log_preprc = log_preprocessor
        self._ancestors = ancestors
        self._location_dao = location_dao

    def process(self, raw_log):
        """
        raw_log: {}
        Returns: Tupple (current_final_log, old_final_log). INSERT: ({}, None), UPDATE ({}, {}), DELETE (None, {})
        """
        current_final_log = None 
        old_final_log = None
        self._log_preprc.preprocess_raw_log(raw_log)
        oper = raw_log["oper"]

        if oper == OPER_INSERT:
            current_final_log = self._insert(raw_log)

        elif oper == OPER_UPDATE:
            current_final_log, old_final_log = self._update(raw_log)

        elif oper == OPER_DELETE:
            old_final_log = self._delete(raw_log)

        else:
            raise FinalLogProcessorException("unknown log operation code %s" %oper) 

        return oper, current_final_log, old_final_log

    def _insert(self, raw_log):
        """
        sample raw log: {
            "_id": ObjectId(""),
            "id": 123,
            "origId": 0,
            "oper": "i",
            "createUTC": ISODate("2011-06-08T23:31:31.491Z"),
            "update": ISODate("2011-06-08T23:31:31.491Z"),
            "source": "client.iphone",
            "userId":"QWERTY",
            "start": ISODate("2011-06-08T23:31:31.491Z"),
            "end": ISODate("2011-06-08T23:31:31.491Z"),
            "text": <string>,
            "location": <string>,
            "nodes": [{"nodeId":<integer>, "metricId": <integer>, "value":<integer|string>}]}
        }
        """
        clean_nodes = []

        for node in raw_log["nodes"]:
            clean_nodes.append({
                                "nodeId":node["nodeId"], 
                                "metricId":node["metricId"], 
                                "value": node["value"]
                                })

        if "update" in raw_log:
            update = raw_log["update"]
        else: 
            update = DateFormatter.to_datetime(raw_log["start"])

        try:
            location = self._get_location(raw_log)
        except Exception, e:
            self._logger.error("## get_location() %s, raw_log: %s" %(e, raw_log))
            location = None

        start = DateParser.from_datetime(raw_log["start"]) if (raw_log["start"] != None and len(str(raw_log["start"]))>0) else None  
        end = DateParser.from_datetime(raw_log["end"]) if (raw_log["end"] != None and len(str(raw_log["end"]))>0) else None  

        final_log = self._final_log_dao.insert_final_log(raw_log["id"], raw_log["oper"], raw_log["createUTC"], update, raw_log["userId"], raw_log["text"], start, end, raw_log["source"], location, clean_nodes)
        self._ancestors.add_ancestors_to_final_log(final_log)

        return final_log

    def _update(self, raw_log):
        old_final_log = self._delete(raw_log)
        current_final_log = self._insert(raw_log)
        self._ancestors.add_ancestors_to_final_log(old_final_log)
        self._ancestors.add_ancestors_to_final_log(current_final_log)

        return current_final_log, old_final_log

    def _delete(self, raw_log):
        """
        sample raw log: {
            "_id": ObjectId(""),
            "id": 123,
            "origId": 456,
            "userId": "8MPLXE",
            "oper": "d",
            "createUTC": ISODate("2011-06-08T23:31:31.491Z"),
            "source": "client.iphone",
        }
        """
        old_final_log = self._final_log_dao.get_final_log_by_id(raw_log["origId"])

        if old_final_log == None:
            raise FinalLogProcessorException("old_final_log not found. original_entry: %s" %raw_log["origId"])

        self._final_log_dao.delete_final_log(old_final_log["_id"])
        self._ancestors.add_ancestors_to_final_log(old_final_log)

        return old_final_log

    def _get_location(self, raw_log):
        #TODO

        country_name = None
        region_name = None
        city_name = None
        
        for node in raw_log["nodes"]:
            if node["nodeId"] == 1162:
                country_name = node["value"]
            if node["nodeId"] == 1164:
                region_name = node["value"]
            if node["nodeId"] == 1166:
                city_name = node["value"]
        
        if city_name:
            name = city_name
            fclass = "P"

        elif region_name:
            name = region_name
            fclass = "A"

        elif country_name:
            name = country_name
            fclass = "A"
        
        else:
            return None    

        location = self._location_dao.search_location(name=name, feature_class=fclass, limit=1)
        if location!=None and len(location)>0:
            return location[0]
        
        return None 
    
    """ Initialization related methods """

    def initialize(self, days_offset):
        flprc_status_mo = self._flprc_status_dao.get_status()

        if flprc_status_mo == None:
            raise FinalLogProcessorException("ERROR: Final Log Processor is not registered. Must be running to be initilized.")

        if flprc_status_mo[LAST_INITIALIZED_RAW_LOG_UTC_FIELD] != None:
            date_from = flprc_status_mo[LAST_INITIALIZED_RAW_LOG_UTC_FIELD]
        else:
            date_from = self._log_dao.get_first_log()[CREATE_UTC_FIELD]

        date_to = DateUtils.add_days(date_from, days_offset)
        raw_logs_cursor = self._log_dao.get_logs_by_create_datetime_utc_range_asc(date_from, date_to)
        raw_logs_count = raw_logs_cursor.count()

        if raw_logs_count == 0:
            raise FinalLogProcessorException("ERROR: No raw logs.")

        print "Processing %s raw logs" %raw_logs_count
        print "from %s" %date_from
        print "to %s ..." %date_to

        start_time = time.time()

        for raw_log in raw_logs_cursor:
            try:
                self.process(raw_log)

            except Exception, e:
                self._logger.error("## %s, raw_log: %s" %(e, raw_log))
                self._logger.exception(e)

            finally:
                self._flprc_status_dao.update_last_initialized_raw_log_datetime_utc(raw_log[CREATE_UTC_FIELD])

        print "\nSUCCESS elapsed time: %s seconds \n" %(time.time()-start_time)
