# coding: utf-8
import os
from sunday.core.cmdexec import cmdexec
from sunday.core.common import exit
from sunday.core.globalvar import getvar
from sunday.core.globalKeyMaps import sdvar_logger

root_key = 'SUNDAY_ROOT'
path_key = 'PATH'
sunday_root = os.environ.get(root_key) or os.path.join(os.environ['HOME'], '.sunday')
sunday_bin = os.path.join(sunday_root, 'bin')
(sign, *_) = cmdexec('which sunday_install')
if sign != 0:
    cur = os.path.abspath(__file__)
    while not os.path.exists(os.path.join(cur, 'bin/sunday_install')) and cur != '/':
        cur = os.path.dirname(cur)
    if cur != '/':
        sunday_bin += ':%s' % os.path.join(cur, 'bin')
    else:
        exit('sunday已安装，但未找到sunday_install执行目录，请检查！')
exportList = ['# sunday']
if not os.environ.get(root_key):
    exportList.append('export %s=%s' % (root_key, sunday_root))
if os.environ.get(path_key).find(sunday_bin) == -1:
    exportList.append('export %s=%s:\$PATH' % (path_key, sunday_bin))

def getShellRcPath():
    shell = os.path.basename(os.environ.get('SHELL') or '')
    p = ''
    if shell == 'zsh':
        p = '.zshrc'
    elif shell == 'bash':
        p = '.bashrc'
    if p: return os.path.join(os.environ['HOME'], p)
    return False

rctext = '\n'.join(exportList)
rcfile = getShellRcPath()
if rcfile and len(exportList) > 1:
    if not os.path.exists(rcfile): cmdexec('touch %s' % rcfile)
    cmdexec('echo "\n%s" >> %s' % (rctext, rcfile))
    getvar(sdvar_logger).info('sunday 初始化成功！')
else:
    print(rctext)
