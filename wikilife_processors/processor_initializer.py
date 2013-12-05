# coding=utf-8

from wikilife_processors.processors.base_user_processor import BaseUserProcessor


class ProcessorInitializerException(Exception):
    pass


class ProcessorInitializer(object):
    """
    """
    
    def __init__(self, logger, flprc_class_fullname, prc_builder):
        self._logger = logger
        self._flprc_class_fullname = flprc_class_fullname
        self._prc_builder = prc_builder

    def initialize_final_logs_processor(self, days_offset):
        """
        days_offset: Integer. Days after.
        """
        processor = self._prc_builder.build_final_log_processor(self._flprc_class_fullname)
        processor.initialize(days_offset)

    def initialize_processor(self, prc_id, days_offset):
        """
        prc_id: String. processor_class_fullname
        days_offset: Integer. Days before processor since date.
        """
        if prc_id == self._flprc_class_fullname:
            raise ProcessorInitializerException("ERROR: Use the correct command to initialize the final log processor.")

        processor = self._prc_builder.build_processor(prc_id)
        processor.initialize(days_offset)

    def initialize_processor_by_user(self, prc_id, user_id, days_offset):
        """
        prc_id: String. processor_class_fullname
        user_id: Internal user id
        """
        if prc_id == self._flprc_class_fullname:
            raise ProcessorInitializerException("ERROR: Use the correct command to initialize the final log processor.")

        processor = self._prc_builder.build_processor(prc_id)
        
        if not isinstance(BaseUserProcessor, processor):
            raise ProcessorInitializerException("ERROR: Only User Based processors can be initialized by user.")

        processor.initialize_by_user(user_id, days_offset)

    def deinitialize_processor_by_user(self, prc_id, user_id):
        """
        prc_id: String. processor_class_fullname
        user_id: Internal user id
        """

        if prc_id == self._flprc_class_fullname:
            raise ProcessorInitializerException("ERROR: Use the correct command to deinitialize the final log processor.")

        processor = self._prc_builder.build_processor(prc_id)
        
        if not isinstance(BaseUserProcessor, processor):
            raise ProcessorInitializerException("ERROR: Only User Based processors can be deinitialized by user.")

        processor.remove_by_user(user_id)
