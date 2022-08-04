# coding: utf-8
import os
import sys
import re
import json
from pydash import pick as _pick
from sunday.core.globalvar import getvar
from sunday.core.globalKeyMaps import sdvar_logger

def clear():
    """清理屏幕"""
    os.system('clear')

def exit(str = ''):
    """退出程序"""
    if str: getvar(sdvar_logger).error(str)
    sys.exit(1)

def pascal_to_snake(camel_case):
    """驼峰转蛇形"""
    snake_case = re.sub(r"(?P<key>[A-Z])", r"_\g<key>", camel_case)
    return snake_case.lower().strip('_')

def snake_to_pascal(snake_case):
    """蛇形转驼峰"""
    words = snake_case.split('_')
    return ''.join(word.title() for word in words)

def parseJson(jsonPath, defaultValue={}, keywords=[], logger=None):
    """传入json文件，返回解析后的数据"""
    if not logger: logger = getvar(sdvar_logger)
    if not os.path.exists(jsonPath): return defaultValue
    with open(jsonPath) as f:
        try:
            content = json.load(f)
            if type(defaultValue) == dict:
                return _pick(content, keywords)
            elif type(defaultValue) == list:
                return [_pick(cont, keywords) for cont in content]
        except Exception as e:
            logger.error('读取文件失败(%s): %s' % (jsonPath, e))
        return defaultValue
