# coding: utf-8
import os
import types

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
