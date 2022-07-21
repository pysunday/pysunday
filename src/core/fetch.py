# coding: utf-8
import requests
from http.cookiejar import LWPCookieJar
from .getConfig import getConfig
from .checkWifi import checkWifi
from .getEnv import getEnv
from .logger import Logger
from pypac import PACSession
from requests.auth import HTTPProxyAuth
import os, sys

# 关闭由verify=False引起的提示
requests.packages.urllib3.disable_warnings()

headers = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'),
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

headers_post = {
    'contentType': {
        'Content-Type': 'application/json;charset=UTF-8'
    }
}

logger = Logger('Fetch').getLogger()
class Fetch():
    def __init__(self, pacWifiName = None):
        self.pacWifiName = pacWifiName
        self._hasProxy = False
        self._hasPacProxy = False
        self.session = self.get_session()

    def get_session(self):
        # 返回session
        proxy = getConfig('PROXY')('proxy')
        session = requests.session() if proxy else PACSession()
        self.openProxy(session, proxy)
        session.headers.update(headers)
        session.verify = False
        return session
    
    def openProxy(self, session, proxy):
        '''开启代理'''
        if proxy:
            logger.warning('存在代理%s' % proxy)
            session.proxies = {
                'http': proxy,
                'https': proxy
            }
            self._hasProxy = True
        else:
            self.openPacProxy(session)
    
    def add_header(self, headers):
        '''更新请求头'''
        if type(headers) == dict:
            self.session.headers.update(headers)
    
    def closeProxy(self):
        '''关闭代理'''
        self.session.proxies = None
        self._hasProxy = False
    
    def hasProxy(self):
        '''返回是否开启代理'''
        return self._hasProxy

    def hasPacProxy(self):
        '''返回是否开启pac'''
        return self._hasPacProxy

    def openPacProxy(self, session):
        '''检测为内网环境则增加代理认证'''
        UM_USER = getEnv('UM_USER')
        UM_PASS = getEnv('UM_PASS')
        if UM_USER and UM_PASS and checkWifi(self.pacWifiName):
            logger.warning('pac认证网络%s' % self.pacWifiName)
            session.proxy_auth = HTTPProxyAuth(UM_USER, UM_PASS)
            self._hasPacProxy = True
            return True
        return False

    def requestByType(self, type, times, *args, **kwargs):
        try:
            res = getattr(self.session, type)(*args, **kwargs)
            logger.info('fetch result %s:%d' % (res.url, res.status_code))
            return res
        except Exception as e:
            if times >= 3:
                logger.error('第%d次尝试失败, 请检查网络后重试!' % times)
                sys.exit(1)
            times += 1
            logger.warning('接口请求失败, 进行第%d次尝试: %s' % (times, e))
            return self.requestByType(type, times, *args, **kwargs)
    
    def get(self, *args, **kwargs):
        return self.requestByType('get', 0, *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.requestByType('post', 0, *args, **kwargs)
    
    def getCookiesDict(self):
        '''cookie转换成对象后返回'''
        cookies = self.session.cookies
        if 'get_dict' in cookies:
            return cookies.get_dict()
        return requests.utils.dict_from_cookiejar(cookies)

