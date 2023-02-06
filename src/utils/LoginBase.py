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
    """
    LoginBase为登录插件开发必须的原始类，供登录插件继承

    **Usage:**

    ```python
    from sunday.utils.LoginBase import LoginBase
    class MyLogin(LoginBase):
        def __init__(self, useLoginState=True, ident=None):
            self.logger = Logger('MyLogin').getLogger()
            LoginBase.__init__(self, logger=self.logger, ident=ident or '', error=[99999, '网站接口异常，请稍后重试'])
            checkUrl = 'http://host:port/getCurrentUser'
            self.rs, self.isLogin = self.initRs(checkUrl, useLoginState)
    ```

    **Parameters:**

    * **logger:** `Logger` -- 子类调用传入，可以保持日志打印一致
    * **pacWifi:** `str` -- wifi名称，如果当前网络连入的wifi相同则使用pac代理
    * **pacUrl:** `str` -- url地址，尝试请求该url，如果能请求到则使用pac代理，一般为内网链接
    * **ident:** `str` -- 多用户标识，用于多用户认证
    * **error:** `list` -- 数组元素为两个时生效，与`sunday.core.fetch.Fetch.setJsonError`入参值一致
    * **file(已弃用):** `str` -- 目标登录对象执行文件
    """
    def __init__(self, file=paths.cacheCwd, logger=Logger('LoginBase').getLogger(), pacWifi=None, pacUrl=None, ident='', error=[]):
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
        """
        程序默认的登录成功判断方法, 即: 请求首页, 如果跳到登录页则说明登录态失效

        这种判断方式根据目标网站处理逻辑不同可能会不准确，一般子类会重构这个方法

        **Parameters:**

        * **checkUrl:** `str` -- 用于检查是否登录成功的网站链接
        """
        if checkUrl is None:
            raise getvar(sdvar_exception)(-1, '检查登录状态的链接不能为空')
        self.fetch.get(checkUrl)
        res = self.fetch.get(checkUrl)
        return res.status_code != 200 or res.url != checkUrl

    def initRs(self, checkUrl=None, useHistory=True):
        """
        初始化会话

        **Parameters:**

        * **checkUrl:** `str` -- 用于检查是否登录成功的网站链接
        * **useHistory:** `bool` -- 标记是否使用上一次的登录态，为False则为重新登录不用历史登录态
        """
        session = self.fetch.session
        session.cookies, isLogin = self.getCookie(useHistory=useHistory)
        if isLogin and self.checkLogin(checkUrl):
            session.cookies, isLogin = self.getCookie(useHistory=False)
        return self.fetch, isLogin

