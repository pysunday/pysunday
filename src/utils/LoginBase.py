# coding: utf-8
import os
import requests
import sunday.core.paths as paths
import sunday.core.globalvar as globalvar
from http.cookiejar import LWPCookieJar, CookieJar
from sunday.core.getConfig import getConfig
from sunday.core.logger import Logger
from sunday.core.fetch import Fetch
from sunday.core.getException import getException
from sunday.core.globalvar import getvar, setvar
from sunday.core.globalKeyMaps import sdvar_exception
from sunday.utils.tools import mergeObj
from pydash import get

LoginError = getException()

class LoginBase():
    def __init__(self, file=paths.cacheCwd, logger=Logger('LoginBase').getLogger(), pacWifi=None, pacUrl=None, ident='', error=[]):
        '''
        file: 目标登录对象执行文件
        logger: 日志对象，用于日志打印
        pacWifi: 匹配的wifi开启pac代理
        pacUrl: 匹配的url开启pac代理
        ident: 多用户标识，用于多用户认证
        '''
        pwd = os.path.abspath(file)
        if os.path.isdir(pwd) == False: pwd = os.path.dirname(pwd)
        self.logger = logger
        cfg = getConfig('LOGIN')
        ident = ('-' if ident else '') + ident
        self.cookiePwd = os.path.join(pwd, cfg('cookieFile') + ident)
        self.envPwd = os.path.join(pwd, cfg('envFile') + ident)
        self.fetch = Fetch(pacWifi=pacWifi, pacUrl=pacUrl)
        if len(error) == 2: self.fetch.setJsonError(*error)

    def getCookiePwd(self):
        return self.cookiePwd

    def getEnvPwd(self):
        return self.envPwd

    def saveCookie(self):
        '''保存cookie'''
        savefun = get(self.fetch, 'session.cookies.save')
        if callable(savefun): savefun(ignore_discard=True, ignore_expires=True)

    def getCookie(self, useHistory=True):
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
        if hasCookieFile: os.remove(filename)
        self.logger.debug('是否存在登录态: 否')
        return LWPCookieJar(filename=filename), False

    def setCookie(self, name, value, domain, rest={}, **argvs):
        '''增加新的cookie, 入参参考cookielib.Cookie中的定义'''
        cookies = self.fetch.session.cookies
        standard = mergeObj({ 'path': '/', 'domain': domain, 'version': 0 }, argvs)
        cookie = CookieJar()._cookie_from_cookie_tuple((name, value, standard, rest), None)
        cookies.set_cookie(cookie)
    
    def checkLogin(self, checkUrl=None):
        '''确认是否登录成功, 方法: 请求首页, 如果跳到登录页则说明登录态失效'''
        # 服务端存在缓存因此请求两次
        if checkUrl is None:
            raise getvar(sdvar_exception)(-1, '检查登录状态的链接不能为空')
        self.fetch.get(checkUrl)
        res = self.fetch.get(checkUrl)
        return res.status_code != 200 or res.url != checkUrl

    def initRs(self, checkUrl=None, useHistory=True):
        """
        checkUrl: 检查登录的链接
        useHistory: 是否使用历史，为False则为重新登录不用历史登录态
        """
        session = self.fetch.session
        session.cookies, isLogin = self.getCookie(useHistory=useHistory)
        if isLogin and self.checkLogin(checkUrl):
            session.cookies, isLogin = self.getCookie(useHistory=False)
        return self.fetch, isLogin

