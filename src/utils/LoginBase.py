# coding: utf-8
import requests
from http.cookiejar import LWPCookieJar, CookieJar
from sunday.core import getConfig, Logger, Fetch, globalvar
from sunday.utils.tools import mergeObj
import os


class LoginBase():
    def __init__(self, file, logger=Logger('LoginBase').getLogger()):
        pwd = os.path.dirname(os.path.abspath(file))
        self.logger = logger
        cfg = getConfig('LOGIN')
        self.cookiePwd = os.path.join(pwd, cfg('cookieFile'))
        self.envPwd = os.path.join(pwd, cfg('envFile'))
        self.fetch = Fetch(pacWifiName = ['PA_WLAN'])

    def getCookiePwd(self):
        return self.cookiePwd

    def getEnvPwd(self):
        return self.envPwd

    def saveCookie(self):
        '''保存cookie'''
        self.fetch.session.cookies.save(ignore_discard=True, ignore_expires=True)

    def getCookie(self, useHistory = True):
        """ params(useHistory): 控制是否使用历史登陆态
            return(cookies, boolean): 返回cookie对象和是否登录标志
        """
        filename = self.getCookiePwd()
        hasCookieFile = os.path.isfile(filename)
        if useHistory and hasCookieFile:
            load_cookiejar = LWPCookieJar()
            load_cookiejar.load(filename, ignore_discard=True, ignore_expires=True)
            load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
            self.logger.debug('是否存在登录态: 是')
            return requests.utils.cookiejar_from_dict(load_cookies), True
        self.logger.debug('是否存在登录态: 否')
        return LWPCookieJar(filename=filename), False

    def setCookie(self, name, value, domain, rest={}, **argvs):
        '''增加新的cookie, 入参参考cookielib.Cookie中的定义'''
        cookies = self.fetch.session.cookies
        standard = mergeObj({ 'path': '/', 'domain': domain, 'version': 0 }, argvs)
        cookie = CookieJar()._cookie_from_cookie_tuple((name, value, standard, rest), None)
        cookies.set_cookie(cookie)
    
    def checkLogin(self, checkUrl):
        '''确认是否登录成功, 方法: 请求首页, 如果跳到登录页则说明登录态失效'''
        # 服务端存在缓存因此请求两次
        self.fetch.get(checkUrl)
        res = self.fetch.get(checkUrl)
        return res.status_code != 200 or res.url != checkUrl

    def initRs(self, checkUrl):
        session = self.fetch.session
        session.cookies, isLogin = self.getCookie()
        if isLogin and self.checkLogin(checkUrl):
            session.cookies, isLogin = self.getCookie(useHistory = False)
        return self.fetch, isLogin

