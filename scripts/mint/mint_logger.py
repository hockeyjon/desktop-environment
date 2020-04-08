
import os
import logging
from logging import *

CONSOLE_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s.%(funcName)s' \
                 ' - %(lineno)s - %(message)s'
FILE_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s.%(funcName)s ' \
              '- %(lineno)s - %(message)s'
DEFAULT_LEVEL = logging.DEBUG


class Logger(logging.Logger):
    """
        Logger class

        :Description: Provides logging library and format.
    """

    def __init__(self, logid, level=DEFAULT_LEVEL):
        """
        Description: Initializes a logger instance with console and file
                     handlers.

            :param logid:       The prefix for the logfile name


            :returns: None

        """
        self.level = level
        self.logid = logid
        logfile = "{}.log".format(self.logid)

        self.log = logging.Logger.__init__(self, self.logid)

        # Create handlers
        consol_handler = logging.StreamHandler()
        self.set_handler(consol_handler, CONSOLE_FORMAT)
        file_handler = logging.FileHandler(logfile)
        self.set_handler(file_handler, FILE_FORMAT)

    def set_handler(self, handler, format):
        handler_formatted = logging.Formatter(format)
        handler.setLevel(self.level)
        handler.setFormatter(handler_formatted)
        self.addHandler(handler)
