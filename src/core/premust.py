# coding: utf-8
import sunday.core.paths as paths
import atexit
import time
import stat
from sunday.core.common import parseJson
from os import path, remove, symlink, listdir, readlink, access, X_OK, chmod
from sunday.core.inner import grenLoginAndToolsInit
from sunday.core.globalvar import getvar, setvar
from sunday.core.logger import Logger
from sunday.core.globalKeyMaps import sdvar_premust, sdvar_logger, sdvar_exectime

__all__ = []

def checkModuleExist():
    # 核对插件存在情况
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

def checkCommandExist():
    # 核对命令软链是否合法
    cmdList = filter(path.islink, map(lambda name:
        path.join(paths.binCwd, name), listdir(paths.binCwd)))
    for cmd in cmdList:
        target = readlink(cmd)
        if not path.exists(target):
            remove(cmd)
            logger.warning('命令不存在软链存在, 删除软链 %s' % path.basename(cmd))
        elif not access(target, X_OK):
            # 原文件无权限则添加执行权限
            chmod(target, stat.S_IRWXU)

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
    checkCommandExist()
    @atexit.register
    def exitPrintExecInfo():
        _, totalExecTime = exectime()
        logger.info('program execution time %.2f s' % totalExecTime)
