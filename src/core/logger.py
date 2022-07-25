# coding: utf-8
import logging
import colorlog
import atexit
import datetime
from os import path
from sunday.core.globalvar import getvar, setvar
from sunday.core.getConfig import getConfig
from sunday.core.paths import logCwd

if not getvar('loggerId'):
    loggerId = datetime.datetime.today().isoformat()
    setvar('loggerId', loggerId)
    @atexit.register
    def exitPrintLogfile():
        print('日志文件: %s' % path.join(logCwd, loggerId))

logfile = path.join(logCwd, getvar('loggerId'))

logging.basicConfig(filename=logfile, level=logging.DEBUG, force=True,
        format='[%(asctime)s.%(msecs)-3d] %(levelname)s <%(name)s>: %(message)s')

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
