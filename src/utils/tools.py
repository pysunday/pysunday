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

def parseJsonp(text):
    # 解析jsonp数据返回dict数据
    import json5
    start = text.find('(') + 1
    end = text.rfind(')')
    return json5.loads(text[start:end])

def currentTimestamp():
    # 当前时间戳
    return int(datetime.timestamp(datetime.now()) * 1000)
