# coding: utf-8

if globals().get('_global_var') is None:
    global _global_var
    _global_var = {}

def getvar(name):
    """
    根据内部全局常量名返回值

    **Parameters:**

    * **name:** `str` -- 全局常量键名
    """
    return _global_var.get(name)

def setvar(name, value):
    """
    设置内部全局常量值

    **Parameters:**

    * **name:** `str` -- 全局常量键名
    * **value:** `str` -- 全局常量值
    """
    _global_var[name] = value
