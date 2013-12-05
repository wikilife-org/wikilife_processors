# coding=utf-8

class ProcessorBuilder(object):

    def __init__(self, logger, daos, log_preprocessor, ancestors):
        self._logger = logger
        self._daos = daos
        self._log_preprocessor = log_preprocessor
        self._ancestors = ancestors

    def build_final_log_processor(self, flprc_class_fullname):
        FLProcessorClass = self._get_class(flprc_class_fullname)
        flprocessor = FLProcessorClass(flprc_class_fullname, self._logger, self._daos.log_dao, self._daos.final_log_dao, self._daos.location_dao, self._daos.flprc_status_dao, self._log_preprocessor, self._ancestors)
        return flprocessor

    def build_processor(self, processor_class_fullname):
        ProcessorClass = self._get_class(processor_class_fullname)
        processor = ProcessorClass(processor_class_fullname, self._logger, self._daos, self._ancestors)
        return processor

    def build_processor_list(self, processor_class_fullname_list):
        processors = []

        for processors_class_fullname in processor_class_fullname_list:
            processor = self.build_processor(processors_class_fullname)
            processors.append(processor)   

        return processors

    def _get_class(self, kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )

        for comp in parts[1:]:
            m = getattr(m, comp)

        return m
