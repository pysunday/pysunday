# coding: utf-8

if globals().get('_global_var') is None:
    global _global_var
    _global_var = {}

def getvar(name):
    '''返回全局变量值'''
    return _global_var.get(name)

def setvar(name, value):
    '''设置全局变量值'''
    _global_var[name] = value
