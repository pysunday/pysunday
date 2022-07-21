# coding: utf-8
import sunday
from os import path, makedirs
from .getEnv import getEnv
from dotenv import load_dotenv

__all__ = ['rootCwd', 'binCwd', 'envCwd', 'sundayLoginCwd', 'sundayToolsCwd']

# sunday家目录
userHomeCwd = path.expanduser('~')
rootCwd = getEnv('SUNDAY_ROOT') or path.join(userHomeCwd, '.sunday')
homePluginsCwd = path.join(rootCwd, 'plugins')
binCwd = path.join(rootCwd, 'bin')
envCwd = path.join(rootCwd, '.env')
path.exists(envCwd) and load_dotenv(envCwd)

for p in [binCwd, homePluginsCwd]:
    if not path.exists(p): makedirs(p)

# sunday模块目录
#pathsCwd = path.realpath(__file__)
#sundayCwd = path.abspath(path.join(pathsCwd, '../..'))
sundayCwd = path.dirname(sunday.__file__)
sundayLoginCwd = path.join(sundayCwd, 'login')
sundayToolsCwd = path.join(sundayCwd, 'tools')

# 配置文件
configCwd = path.join(rootCwd, 'config.ini')
if not path.exists(configCwd): configCwd = path.join(sundayCwd, 'config.ini')
