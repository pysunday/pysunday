# coding: utf-8
import os

def getEnv(key):
    '''返回键名为key的系统环境变量值'''
    return os.environ.get(key)
