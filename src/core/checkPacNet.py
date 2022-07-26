# coding: utf-8
import re
import subprocess
import requests
from sunday.core.logger import Logger

logger = Logger('checkPacNet').getLogger()

def checkWifi(name):
    '''传入wifi名, 返回当前wifi是否匹配'''
    if not name: return False
    if type(name) == str: name = [name]
    logger.debug('检查wifi: %s' % '、'.join(name))
    command = ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I']
    res = subprocess.check_output(command).decode('utf-8')
    return any(re.search(re.compile('SSID: %s\n' % item), res) for item in name)

def checkUrl(url):
    '''传入链接名, 返回当前网络是否能访问到'''
    if not url: return False
    if type(url) == str: url = [url]
    logger.debug('检查链接: %s' % '、'.join(url))
    def requestUrl(tar):
        try:
            return requests.get(tar).ok
        except:
            return False
    return any(requestUrl(item) for item in url)

def checkPacNet(wifi, url):
    return checkWifi(wifi) or checkUrl(url)
