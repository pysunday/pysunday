# coding: utf-8
import sunday.core.globalvar as globalvar

def cache_name(name: str):
    '''根据名称缓存第一次执行结果。
    Args:
        name(str): 被实例化对象的名称
    Usages:
        @cache_name('test')
        class Test(LoginBase):
            pass
    此后不管实例化多少Test对象都只会返回第一次实例化的结果的引用
    '''
    def cache_name_func(func):
        def wrap(*args, **kwargs):
            if globalvar.getvar(name) is None:
                globalvar.setvar(name, func(*args, **kwargs))
            return globalvar.getvar(name)
        return wrap
    return cache_name_func
