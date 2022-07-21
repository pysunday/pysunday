# coding: utf-8
import os
import sys
import re

def clear():
    """清理屏幕"""
    os.system('clear')

def exit(str = ''):
    """退出程序"""
    if str: print(str)
    sys.exit(1)

def pascal_to_snake(camel_case):
    """驼峰转蛇形"""
    snake_case = re.sub(r"(?P<key>[A-Z])", r"_\g<key>", camel_case)
    return snake_case.lower().strip('_')

def snake_to_pascal(snake_case):
    """蛇形转驼峰"""
    words = snake_case.split('_')
    return ''.join(word.title() for word in words)