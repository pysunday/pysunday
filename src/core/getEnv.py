# coding: utf-8
import os

def getEnv(key):
    '''返回env中对应key的值'''
    return os.environ.get(key)
