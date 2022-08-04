# coding: utf-8
import os
from sunday.core.cmdexec import cmdexec
from sunday.core.common import exit

sunday_root = os.path.join(os.environ['HOME'], '.sunday')
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
rctext = '\n# sunday\nexport SUNDAY_ROOT=%s\nexport PATH=%s:\$PATH' % (sunday_root, sunday_bin)

for rc in ['.bashrc', '.zshrc']:
    rcfile = os.path.join(os.environ['HOME'], rc)
    if not os.path.exists(rcfile): cmdexec('touch %s' % rcfile)
    cmdexec('echo "%s" >> %s' % (rctext, rcfile))
