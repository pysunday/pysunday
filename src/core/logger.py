# coding: utf-8
import logging
import colorlog
from .getConfig import getConfig

class Logger():
    def __init__(self, name, level='', format=''):
        cfg = getConfig('LOGGING')
        logger = logging.getLogger(name)
        logger.setLevel(logging.getLevelName(level or cfg('level')))
        loghd = logging.StreamHandler()
        loghd.setFormatter(colorlog.ColoredFormatter(format or cfg('format'), datefmt='%H:%M:%S'))
        logger.addHandler(loghd)
        logger.propagate = True
        self.logger = logger
    
    def getLogger(self):
        return self.logger