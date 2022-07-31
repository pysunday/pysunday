# coding: utf-8
import sunday.core.paths as paths
from sunday.core.common import parseJson
from os import path, remove, symlink
from sunday.core.inner import grenLoginAndToolsInit
from sunday.core.globalvar import getvar, setvar
from sunday.core.logger import Logger

__all__ = []


def checkModuleExist():
    changeFlag = False
    logger = getvar('sunday_logger')
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

if not getvar('sunday_premust'):
    setvar('sunday_premust', True)
    setvar('sunday_logger', Logger('SUNDAY').getLogger())
    checkModuleExist()
