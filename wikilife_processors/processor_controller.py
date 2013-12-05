# coding=utf-8

from wikilife_utils.date_utils import DateUtils

class ProcessorControllerException(Exception):
    pass

class ProcessorController(object):
    """
    Pops queue and send messages to processors.
    """

    _logger = None
    _flprc_class_fullname = None
    _prc_class_fullname_list = None
    _prc_status_dao = None
    _flprc_status_dao = None
    _prc_builder = None
    _queue_consumer = None
    _flprc = None
    _prcs = None

    def __init__(self, logger, flprc_class_fullname, prc_class_fullname_list, prc_status_dao, flprc_status_dao, prc_builder, queue_consumer):
        self._logger = logger
        self._flprc_class_fullname = flprc_class_fullname 
        self._prc_class_fullname_list = prc_class_fullname_list
        self._prc_status_dao = prc_status_dao
        self._flprc_status_dao = flprc_status_dao
        self._prc_builder = prc_builder
        self._queue_consumer = queue_consumer

    def start(self):
        """
        Start listening for messages from the Rabbit Queue
        """
        self._flprc = self._prc_builder.build_final_log_processor(self._flprc_class_fullname)
        self._prcs = self._prc_builder.build_processor_list(self._prc_class_fullname_list)
        self._register_final_log_processor()
        self._register_processors()
        self._queue_consumer.start(self._process)

    def _process(self, raw_log):
        try:
            #NOTE: to scale must add a front queue for the final_log_prc and n subsequent queues with log prcs 
            oper, current_final_log, old_final_log = self._flprc.process(raw_log)

            for processor in self._prcs:
                try:
                    processor.execute(oper, current_final_log, old_final_log)

                except Exception, e:
                    self._logger.error("## prc: %s, raw_log: %s, oper: %s, current_final_log: %s, old_final_log: %s" %(processor.__class__, raw_log, oper, current_final_log, old_final_log))
                    self._logger.exception(e)

        except Exception, e:
            self._logger.error("## raw_log: %s" %raw_log)
            self._logger.exception(e)

        return True

    def _register_final_log_processor(self):
        status = self._flprc_status_dao.get_status()
        if status == None:
            self._flprc_status_dao.insert_status(self._flprc_class_fullname, DateUtils.get_datetime_utc())

    def _register_processors(self):
        del_ids = self._prc_status_dao.delete_processors_status_except(self._prc_class_fullname_list)
        print "Deleted processors: %s\n%s" %(len(del_ids), ("\n".join(del_ids))+"\n" if len(del_ids) else "")

        for prc_id in self._prc_class_fullname_list:
            prc = self._prc_status_dao.get_processor_status(prc_id)
            if prc == None:
                self._prc_status_dao.insert_processor_status(prc_id, DateUtils.get_datetime_utc())

        prcs_ids = []
        for prc in self._prc_status_dao.get_processors_status():
            prcs_ids.append(prc["_id"])

        print "Registered processors: %s\n%s" %(len(prcs_ids), "\n".join(prcs_ids))
