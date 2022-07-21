# coding: utf-8
import re
import subprocess

def checkWifi(name):
    '''传入wifi名, 返回当前wifi是否匹配'''
    if not name: return False
    if type(name) == str: name = [name]
    command = ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I']
    res = subprocess.check_output(command).decode('utf-8')
    return any(re.search(re.compile('SSID: %s\n' % item), res) for item in name)
