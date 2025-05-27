# coding: utf-8
import os
import sys
from dotenv import load_dotenv, get_key, set_key, unset_key
from sunday.core.logger import Logger

logger = Logger('enver').getLogger()

def enver(file: str):
    '''传入env文件, 返回操作env文件的方法
    Args:
        file(str): 文件路径
    Returns:
        getenv(key): 获取键对应的值
        setenv(key, val): 设置键和值
        getfile(): 返回当前env文件路径
    Usages:
        getenv, setenv, = enver('./.env')
        getenv('key')
        setenv('key', 'val')
    '''
    if not os.path.exists(os.path.dirname(file)):
        logger.error('路径目录不存在 %s' % file)
        sys.exit(1)
    if not os.path.isfile(file):
        logger.debug('新建文件 %s' % file)
        os.system('touch %s' % file)
    load_dotenv(file)
    def getenv(key):
        '''返回env中对应key的值'''
        return get_key(file, str(key))
    def setenv(key, val = None):
        '''设置env中对应key的值'''
        if not val:
            os.environ.pop(key)
            unset_key(file, str(key))
        else:
            set_key(file, str(key), str(val))
    def getfile():
        return file
    return getenv, setenv, getfile
