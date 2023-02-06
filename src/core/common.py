# coding: utf-8
import os
import sys
import re
import json
from pydash import pick as _pick
from sunday.core.globalvar import getvar
from sunday.core.globalKeyMaps import sdvar_logger

def clear():
    """清空屏幕"""
    os.system('clear')

def exit(text=''):
    """
    退出程序

    **Parameters:**

    * **text:** `str` -- 程序退出并打印退出提示文本
    """
    if text: getvar(sdvar_logger).critical(text)
    sys.exit(1)

def pascal_to_snake(text):
    """
    驼峰转蛇形

    **Usage:**

    ```
    >>> from sunday.core.common import pascal_to_snake
    >>> pascal_to_snake('HelloWorld')
    hello_world
    ```

    **Parameters:**

    * **text:** `str` -- 驼峰串
    """
    word = re.sub(r"(?P<key>[A-Z])", r"_\g<key>", text)
    return word.lower().strip('_')

def snake_to_pascal(text):
    """
    蛇形转驼峰

    **Usage:**

    ```
    >>> from sunday.core.common import snake_to_pascal
    >>> snake_to_pascal('hello_world')
    HelloWorld
    ```

    **Parameters:**

    * **text:** `str` -- 蛇形串
    """
    words = text.split('_')
    return ''.join(word.title() for word in words)

def parseJson(jsonPath, defaultValue={}, keywords=[], logger=None):
    """
    传入json文件，返回解析后的json数据

    **Parameters:**

    * **jsonPath:** `str` -- 文件路径
    * **defaultValue:** `list | dict` -- 文件读取失败时返回的默认数据
    * **keywords:** `list` -- 需要的键集合
    * **logger:** `str` -- 日志对象
    """
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
