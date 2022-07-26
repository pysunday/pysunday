# coding: utf-8
import sunday.core.globalvar as globalvar

def cache_name(name):
    '''根据名称缓存第一次执行结果'''
    def cache_name_func(func):
        def wrap(*args, **kwargs):
            if globalvar.getvar(name) is None:
                globalvar.setvar(name, func(*args, **kwargs))
            return globalvar.getvar(name)
        return wrap
    return cache_name_func
