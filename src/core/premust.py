# coding: utf-8
import sunday.core.paths as paths
import atexit
import time
from sunday.core.common import parseJson
from os import path, remove, symlink
from sunday.core.inner import grenLoginAndToolsInit
from sunday.core.globalvar import getvar, setvar
from sunday.core.logger import Logger
from sunday.core.globalKeyMaps import sdvar_premust, sdvar_logger, sdvar_exectime

__all__ = []


def checkModuleExist():
    changeFlag = False
    logger = getvar(sdvar_logger)
    for item in parseJson(paths.moduleLockCwd, [], ['origin', 'target', 'type', 'name']):
        target = item['target']
        origin = item['origin']
        mname = item['name']
        mtype = item['type']
        hasTar = path.islink(target)
        hasOri = path.exists(origin)
        if hasTar and not hasOri:
            # 删除软链
            remove(target)
            changeFlag = True
            logger.warning('插件不存在软链存在, 删除软链 %s/%s' % (mtype, mname))
        elif hasOri and not hasTar:
            # 建立软链
            symlink(origin, target)
            changeFlag = True
            logger.warning('插件存在软链不存在, 创建软链 %s/%s' % (mtype, mname))
    if changeFlag:
        grenLoginAndToolsInit()

def initPrintTime():
    now = time.time()
    vars = { 'firstTime': now, 'preTime': now }
    def printTime():
        nowTime = time.time()
        lastExecTime = nowTime - vars['preTime']
        totalExecTime = nowTime - vars['firstTime']
        vars['preTime'] = nowTime
        return lastExecTime, totalExecTime
    return printTime

if not getvar(sdvar_premust):
    setvar(sdvar_premust, True)
    setvar(sdvar_logger, Logger('SUNDAY').getLogger())
    setvar(sdvar_exectime, initPrintTime())

    logger = getvar(sdvar_logger)
    exectime = getvar(sdvar_exectime)

    checkModuleExist()
    @atexit.register
    def exitPrintExecInfo():
        _, totalExecTime = exectime()
        logger.info('program execution time %.2f s' % totalExecTime)
