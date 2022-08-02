# coding: utf-8
# sunday 内部使用方法
import os
import sunday.core.paths as paths
from sunday.core.cmdexec import cmdexec
from sunday.core.globalvar import getvar
from sunday.core.globalKeyMaps import sdvar_logger
from sunday.core.common import parseJson
import sunday.core.paths as paths

__all__ = ['grenLoginAndToolsInit', 'printAllPlugin']

def grenLoginAndToolsInit():
    """生成插件的init导出文件"""
    logger = getvar(sdvar_logger)
    def grenInitFile(pathname):
        # 修改登录模块的__file__文件导出全部的登录模块
        filename = os.path.join(pathname, '__init__.py')
        filelist = list(filter(lambda n: n not in ['__init__.py', '__init__.pyc', '__pycache__'], os.listdir(pathname)))
        with open(filename, 'w') as f:
            f.write('\n'.join(['from . import %s' % i for i in filelist ]))
        logger.debug('文件内容:\n'.join([filename, cmdexec('cat %s' % filename)[1]]))
    grenInitFile(paths.sundayLoginCwd)
    grenInitFile(paths.sundayToolsCwd)

def printAllPlugin():
    # 打印所有插件信息
    logger = getvar(sdvar_logger)
    plugins = parseJson(paths.moduleLockCwd, [], ['origin', 'target', 'type', 'name'])
    pluginsArr = list(filter(lambda item: os.path.islink(item['target']), plugins))
    pluginsStr = '、'.join([item['type'] + '/' + item['name'] for item in pluginsArr])
    cmdStr = '、'.join(os.listdir(paths.binCwd))
    logger.info('已安装插件: %s' % pluginsStr)
    logger.info('可执行命令: %s' % cmdStr)
