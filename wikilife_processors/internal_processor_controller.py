# coding=utf-8

import sys
import traceback

class InternalProcessorControllerException(Exception):
    pass

class InternalProcessorController(object):
    """
    Pops queue and send messages to internal processors.
    """

    def __init__(self, logger, queue_consumer, oper_prc_map):
        self._logger = logger
        self._queue_consumer = queue_consumer
        self._oper_prc_map = oper_prc_map

    def start(self):
        """
        Start listening for messages from the Rabbit Queue
        """
        self._queue_consumer.start(self._process)

    def _process(self, internal_oper):
        processor = self._oper_prc_map[internal_oper["code"]]

        try:
            processor.process(internal_oper)

        except Exception, e:
            exc_traceback = sys.exc_info()[2]
            self._logger.error("## %s : %s, %s, log: %s" %(processor.__class__, e, traceback.print_tb(exc_traceback), internal_oper))

        return True
