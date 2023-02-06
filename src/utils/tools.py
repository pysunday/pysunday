# coding: utf-8
import os
import types
from datetime import datetime

def mergeObj(ori={}, *objs):
    '''合并字典'''
    newObj = ori.copy()
    for obj in objs:
        newObj.update(obj)
    return newObj


def get_format_str(widths):
    str_width = sum(widths) + (len(widths) - 1) * 3 + 4
    ans = '|'
    for width in widths:
        ans += ' %-{}s'.format(width)
    return ans, str_width

def get_width(ans):
    width = 0
    times = 0
    if type(ans) in [bytes, str]:
        for s in ans:
            if ord(s) > 127:
                times += 1
        width = len(ans) + times
    return width, times

def parseJsonp(text, defvalue={}):
    """
    解析jsonp数据返回dict数据

    **Parameters:**

    * **text:** `str` -- jsonp数据字符串, 格式如：`jsonp_12345({})`
    """
    import json5
    try:
        start = text.find('(') + 1
        end = text.rfind(')')
        return json5.loads(text[start:end])
    except Exception as e:
        defvalue['sunday_msg'] = str(e)
        defvalue['sunday_ok'] = False
        return defvalue

def currentTimestamp():
    """
    返回当前时间戳, 单位为毫秒
    """
    return int(datetime.timestamp(datetime.now()) * 1000)
