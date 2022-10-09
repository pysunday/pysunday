# coding: utf-8
import requests
import time
import sunday.core.paths as paths
from http.cookiejar import LWPCookieJar
from sunday.core.getEnv import getEnv
from sunday.core.logger import Logger
from sunday.core.common import exit
from sunday.core.checkPacNet import checkPacNet
from sunday.core.getConfig import getConfig
from sunday.core.enver import enver
from sunday.core.auth import Auth, getCurrentUser
from pypac import PACSession
from requests.auth import HTTPProxyAuth

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
    def __init__(self, pacWifi = None, pacUrl = None, pacWifiName = None):
        # pacWifiName 兼容老写法
        self.pacWifi = pacWifi or pacWifiName
        self.pacUrl = pacUrl
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
            logger.debug('fetching %s %s' % (args, kwargs))
            res = getattr(self.session, type)(*args, **kwargs)
            logger.info('fetch result %s (状态: %d, 用时: %.3f)' % (res.url, res.status_code, time.time() - stime))
            return res
        except Exception as e:
            if times >= 3:
                exit('第%d次尝试失败, 请检查网络后重试!' % times)
            times += 1
            logger.warning('接口请求失败, 进行第%d次尝试: %s' % (times, e))
            return self.requestByType(type, times, *args, **kwargs)

    def requests_common(self, type, *args, **kwargs):
        res = self.requestByType(type, 0, *args, **kwargs)
        if not res.ok: logger.error('请求结果异常：' % res.text)
        return res
    
    def get(self, *args, **kwargs):
        return self.requests_common('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.requests_common('post', *args, **kwargs)

    def requests_json_common(self, type, *args, **kwargs):
        ans = self.requestByType(type, 0, *args, **kwargs)
        try:
            data = ans.json()
            data.update({ 'text': ans.text })
            return data
        except Exception as e:
            logger.error('请求结果json解析失败: %s' % ans.text)
            return { 'sunday_error': True, 'msg': '返回结果非对象', 'url': ans.request.url, 'text': ans.text, 'type': type }

    # get请求，返回dict对象
    def get_json(self, *args, **kwargs): return self.requests_json_common('get', *args, **kwargs)

    # post请求，返回dict对象
    def post_json(self, *args, **kwargs): return self.requests_json_common('post', *args, **kwargs)

    def getCookiesDict(self):
        '''cookie转换成对象后返回'''
        cookies = self.session.cookies
        if 'get_dict' in cookies:
            return cookies.get_dict()
        return requests.utils.dict_from_cookiejar(cookies)
