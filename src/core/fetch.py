# coding: utf-8
import requests
import time
import sunday.core.paths as paths
import validators
from http.cookiejar import LWPCookieJar, CookieJar
from sunday.core.getEnv import getEnv
from sunday.core.logger import Logger
from sunday.core.checkPacNet import checkPacNet
from sunday.core.getConfig import getConfig
from sunday.core.enver import enver
from sunday.core.auth import Auth, getCurrentUser
from pypac import PACSession
from requests.auth import HTTPProxyAuth
from sunday.core.globalvar import getvar, setvar
from sunday.core.globalKeyMaps import sdvar_exception
from pydash import omit, get

# 关闭由verify=False引起的提示
requests.packages.urllib3.disable_warnings()

headers = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'),
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip, deflate',
}

headers_post = {
    'contentType': {
        'Content-Type': 'application/json;charset=UTF-8'
    }
}

logger = Logger('Fetch').getLogger()
class Fetch():
    """
    对requests进行封装，实现内网环境使用系统pac代理、保持会话、请求失败再次尝试、请求代理、返回结果安全json化等

    **Usage:**

    ```
    >>> from sunday.core.fetch import Fetch
    >>> fetch = Fetch()
    >>> fetch.get('https://www.baidu.com')
    <Response [200]>
    ```

    **Parameters:**

    * **pacWifi:** `str` -- wifi名称，如果当前网络连入的wifi相同则使用pac代理
    * **pacUrl:** `str` -- url地址，尝试请求该url，如果能请求到则使用pac代理，一般为内网链接
    * **pacWifiName(弃用):** `str` -- 与pacWifi一致，为了兼容老代码
    * **proxy:** `str` -- 让请求使用代理，传入如：`127.0.0.1:8888`或者`https://127.0.0.1:5555/getProxy`

    **Return:** `fetch`
    """
    def __init__(self, pacWifi=None, pacUrl=None, pacWifiName=None, proxy=None):
        self.pacWifi = pacWifi or pacWifiName
        self.pacUrl = pacUrl
        self._hasProxy = False
        self._proxystr = proxy
        self._hasPacProxy = False
        self.session = self.get_session(proxy)
        self.jsonErrorMessage = None
        self.jsonErrorNumber = 99999

    def setJsonError(self, jsonErrorMessage='服务器异常请稍后重试!', jsonErrorNumber=99999):
        """
        设置get_json与post_json方法中执行json化失败的报错配置，若配置后返回非json数据则直接报错

        **Usage:**

        ```
        >>> from sunday.core.fetch import Fetch
        >>> fetch = Fetch()

        >>> fetch.get('https://www.baidu.com')
        {'sunday_error': True,
         'msg': '返回结果非JSON',
         'url': 'https://www.baidu.com',
         'text': ''}

        >>> fetch.setJsonError()
        >>> fetch.get('https://www.baidu.com')
        CustomError: '99999 服务器异常请稍后重试!'
        ```

        **Parameters:**

        * **jsonErrorMessage:** `str` -- 报错提示信息, 默认`服务器异常请稍后重试!`
        * **jsonErrorNumber:** `int` -- 报错code编码, 默认`99999`
        """
        self.jsonErrorNumber = jsonErrorNumber
        self.jsonErrorMessage = jsonErrorMessage

    def get_session(self, proxy=None):
        # 返回session
        proxy = proxy or getConfig('PROXY')('proxy')
        session = requests.session() if proxy else PACSession()
        self.openProxy(session, proxy)
        session.headers.update(headers)
        session.verify = False
        return session
    
    def openProxy(self, session, proxy):
        '''开启代理'''
        if proxy:
            self._proxystr = proxy
            if validators.url(proxy) == True:
                proxy = requests.get(proxy).text
            prevProxy = get(session, 'proxies.http')
            if prevProxy is None:
                logger.warning(f'设置代理：{proxy}')
            elif prevProxy != proxy:
                logger.warning(f'更换代理：{prevProxy} => {proxy}')
            session.proxies = {
                'http': proxy,
                'https': proxy
            }
            self._hasProxy = True
        else:
            self.openPacProxy(session)
    
    def add_header(self, headers):
        """
        设置全局请求头

        **Parameters:**

        * **headers:** `dict` -- 添加到请求头的字典
        """
        if type(headers) == dict:
            self.session.headers.update(headers)
    
    def closeProxy(self):
        '''关闭代理'''
        self.session.proxies = None
        self._hasProxy = False
    
    def hasProxy(self):
        '''返回是否开启代理'''
        if self._hasProxy != True: return False
        proxy = get(self.session, 'proxies.http'),
        return {
                'hasProxy': self._hasProxy,
                'proxystr': self._proxystr,
                'proxy': proxy,
                'proxytype': None if proxy == self._proxystr else 'url'
                }

    def hasPacProxy(self):
        '''返回是否开启pac'''
        return self._hasPacProxy

    def openPacProxy(self, session):
        '''检测为内网环境则增加代理认证'''
        if checkPacNet(self.pacWifi, self.pacUrl):
            auth = Auth(paths.envCwd, '[PAC PROXY]')
            getenv = enver(paths.envCwd)[0]
            username = auth.addParams('pac_user', 'PAC代理账号', value=getenv('pac_user'), defaultValue=getCurrentUser())
            password = auth.addParams('pac_pass', 'PAC代理密码', value=getenv('pac_pass'), isPass=True)
            logger.warning('pac认证网络, 网络交互使用代理中')
            session.proxy_auth = HTTPProxyAuth(username, password)
            self._hasPacProxy = True
            return True
        return False

    def requestByType(self, type, times, *args, **kwargs):
        try:
            stime = time.time()
            params = omit(kwargs, ['timeout_time'])
            logger.debug('fetching %s %s' % (args, params))
            if 'timeout' not in params: params['timeout'] = 15
            res = getattr(self.session, type)(*args, **params)
            logger.info('fetch result %s (状态: %d, 用时: %.3f)' % (res.url, res.status_code, time.time() - stime))
            return res
        except Exception as e:
            if times >= kwargs.get('timeout_time', 3):
                raise getvar(sdvar_exception)(-1, '第%d次尝试失败, 请检查网络后重试!' % times)
            logger.warning('接口请求失败, 进行第%d次尝试: %s' % (times + 1, e))
            if self._hasProxy and self.hasProxy().get('proxytype') == 'url': self.openProxy(self.session, self.hasProxy().get('proxystr'))
            times += 1
            return self.requestByType(type, times, *args, **kwargs)

    def requests_common(self, type, *args, **kwargs):
        res = self.requestByType(type, 0, *args, **kwargs)
        if not res.ok: logger.error(f'请求结果异常{res.status_code}：{res.text or "无内容"}')
        return res
    
    def get(self, *args, **kwargs):
        """
        发起get请求并对返回结果调用json方法，调用方式与requests.get一致

        **Parameters:**

        * **timeout_time:** `int` -- 超时尝试次数，默认为3次
        """
        return self.requests_common('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        """
        发起post请求并对返回结果调用json方法，调用方式与requests.post一致

        **Parameters:**

        * **timeout_time:** `int` -- 超时尝试次数，默认为3次
        """
        return self.requests_common('post', *args, **kwargs)

    def requests_json_common(self, type, *args, **kwargs):
        ans = self.requestByType(type, 0, *args, **kwargs)
        try:
            data = ans.json()
            if hasattr(data, 'update'):
                data.update({ 'text': ans.text })
                return data
            return {
                    'data': data,
                    'text': ans.text,
                    }
        except Exception as e:
            logger.error('请求结果json解析失败: %s' % ans.text)
            if self.jsonErrorMessage: raise getvar(sdvar_exception)(self.jsonErrorNumber, self.jsonErrorMessage)
            return { 'sunday_error': True, 'msg': '返回结果非JSON', 'url': ans.request.url, 'text': ans.text, 'type': type }

    # get请求，返回dict对象
    def get_json(self, *args, **kwargs):
        """
        发起get请求并对返回结果调用json方法，调用方式与requests.get一致，由于对json方法做了安全处理建议在预期返回json数据的接口使用

        **Parameters:**

        * **timeout_time:** `int` -- 超时尝试次数，默认为3次
        """
        return self.requests_json_common('get', *args, **kwargs)

    # post请求，返回dict对象
    def post_json(self, *args, **kwargs):
        """
        发起post请求并对返回结果调用json方法，调用方式与requests.post一致，由于对json方法做了安全处理建议在预期返回json数据的接口使用

        **Parameters:**

        * **timeout_time:** `int` -- 超时尝试次数，默认为3次
        """
        return self.requests_json_common('post', *args, **kwargs)

    def getCookiesDict(self):
        """
        将cookie转化为字典并返回

        **Return:** `dict`
        """
        cookies = self.session.cookies
        if 'get_dict' in cookies:
            return cookies.get_dict()
        return requests.utils.dict_from_cookiejar(cookies)

    def setCookie(self, name, value, domain, rest={}, **argvs):
        """
        增加新的cookie, 入参参考cookielib.Cookie中的定义

        **Parameters:**

        * **name:** `str` -- cookie键名
        * **value:** `str` -- cookie键值
        * **domain:** `str` -- 主机名
        """
        cookies = self.session.cookies
        standard = { 'path': '/', 'domain': domain, 'version': 0 }
        standard.update(argvs)
        cookie = CookieJar()._cookie_from_cookie_tuple((name, value, standard, rest), None)
        cookies.set_cookie(cookie)
