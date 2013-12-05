# coding=utf-8

from abc import abstractmethod


class BaseInternalProcessorException(Exception):
    pass


class BaseInternalProcessor(object):
    """
    Abstract class
    """

    @abstractmethod
    def process(self, internal_oper):
        raise BaseInternalProcessorException("Unimplemented abstract method")
