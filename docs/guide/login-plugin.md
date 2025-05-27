# 登录插件开发

快速开发登录插件，自动管理登录态，可用户后端服务提供目标登录网站代理服务、目标登录网站命令行工具、需要登录的爬虫等。

---
## 介绍

基于PySunday开发的登录插件会自动管理登录态，支持多用户登录、登录态自动检测、Cookies自动管理。

## 插件讲解

模版仓库地址：https://github.com/pysunday-plugins/login-template

文件结构如下：

```
.
├── __init__.py
├── .source.example
├── error.py
├── login.py
├── package.json
├── README.md
└── requirements.txt
```

### requirements.txt

此处存放插件依赖的第三方包，执行sunday_install命令后会自动安装

### package.json

用于存放项目的基本信息

键名 | 介绍 | 类型 | 默认值
---- | ---- | ---- | ------
name | 插件名称 | str | - 
type | 插件类型 | `tools/login` | login
version | 版本号 | str | -
description | 插件描述 | str | -
bin | 命令行可执行命令 | list | -
depend | 依赖的插件 | list | -
keywords | 关键词 | list |  -
author | | 作者 | str | -

其中type区分是登录插件还是工具插件，配合name的值，最终会生成名为login-name的文件夹

### .source.example

该文件可以存放密码等关键信息，需要手动改名为.source，该文件不会上传github，只要执行`source .source`即可通过工具函数`getEnv`获取

### __init__.py

该文件用于向外提供登录插件用于产线使用时的必要方法。

1. getLoginHandler: 获取登录插件的主体类，当有多个登录模组的时候，需要传入类名全称的字符串
2. getLoginParams: 返回该插件的入参对象, 需要定义paramsKeysMap的键值对应关系，当有多个登录模组的时候，需要传入类名全称
3. checkLoginParams: 传入入参，检查入参是否符合要求并，不符合要求则打印输出并报错

完整代码入：

```python
from .login import *
from .error import TemplateLoginError

paramsKeysMap = {
        'phone': '手机号',
        'password': '密码',
        }

defaultName = 'TemplateLogin'

def getLoginHandler(name=None):
    name = name or defaultName
    return eval(name)

def checkLoginParams(params={}, name=None):
    name = name or defaultName
    mustKeys = eval(f'mustParams{name}')
    if type(mustKeys) == dict: mustKeys = mustKeys.keys()
    notKeys = [key for key in mustKeys if not params.get(key)]
    if len(notKeys) > 0: raise TemplateLoginError(10003, other=','.join(notKeys))
    return { key: params.get(key) for key in mustKeys }

def getLoginParams(name=None):
    name = name or defaultName
    mustKeys = eval(f'mustParams{name}')
    keysMaps = paramsKeysMap.copy()
    if type(mustKeys) == dict:
        keysMaps.update(mustKeys)
        mustKeys = mustKeys.keys()
    return {key: paramsKeysMap.get(key, '未知') for key in mustKeys}
```

### login.py

该文件为登录插件主体代码。文件名不固定，最终在__init__.py文件中导入即可

样例代码如下：

```python
# coding: utf-8
from sunday.utils import LoginBase
from sunday.core import Logger, enver, Auth, getEnv, aesCbcDecrypt, getConfig
from pydash import pick
from .error import errorMap, TemplateLoginError

cryptoKey = getConfig('CRYPTO')('key')

def getUrlMap(url):
    baseUrl = url + '/api'
    return {
            'login': baseUrl + '//login',
            'currentUser': baseUrl + '/profile',
            }

mustParamsTemplateLogin = {
        'phone': '手机号',
        'password': '密码',
        }
class TemplateLogin(LoginBase):
    def __init__(self, phone=None, password=None, isEncrypt=False, useLoginState=True, **_):
        self.logger = Logger('登录').getLogger()
        self.urlMap = getUrlMap('https://user.template.com')
        LoginBase.__init__(self, logger=self.logger, ident=phone or '', error=[99999, '接口异常，请稍后重试'])
        self.phone = phone
        self.password = aesCbcDecrypt(password, cryptoKey) if isEncrypt else password
        self.initAuth()
        self.rs, self.isLogin = self.initRs(self.urlMap['currentUser'], useLoginState)

    def initAuth(self):
        auth = Auth(self.getEnvPwd(), '[登录]')
        self.getenv, self.setenv, *_ = enver(self.getEnvPwd())
        auth.addParams('password', value=self.password or self.getenv('password') or '', isPass=False, tip='密码')
        self.auth = auth

    def checkLogin(self, checkUrl):
        try:
            res = self.fetch.get_json(checkUrl)
        except Exception:
            return True
        return res.get('stat') != 1

    def userLogin(self):
        params = self.auth.getParams()
        self.rs.post_json(
                self.urlMap['login'],
                data={
                    "phone": self.phone,
                    "password": params.get('password')
                },
            )

    def getCurrentUser(self):
        res = self.rs.get_json(self.urlMap['currentUser'])
        return pick(res, 'name', 'phone')

    def login(self):
        if self.isLogin:
            self.logger.info('登录成功')
            return self
        self.userLogin()
        if not self.checkLogin(self.urlMap['currentUser']):
            self.logger.info('登录成功')
            self.saveCookie()
            return self
        else:
            self.logger.error(errorMap[10000])
            raise TemplateLoginError(10000)


if __name__ == "__main__":
    template = TemplateLogin(getEnv('SUNDAY_CUS_TEMPLATE_PHONE'), getEnv('SUNDAY_CUS_TEMPLATE_PASSWORD'))
    template.login()
```

其中mustParamsTemplateLogin即可以时数组也可以是对象，用于检测入参是否符合预期使用

TemplateLogin是该插件的主体类，继承自core.LoginBase类，提供基类方法`initRs`，用于检查登录态是否还有效，执行完会返回会话操作实例和是否登录的布尔值，需要注意的是需要重写方法`checkLogin`，用于检测登录态是否还有效。

一般登录插件会请求两个目标网站的接口服务，一个是登录接口，另一个是用户信息接口，通过判断用户信息接口是否能返回当前登录用户信息以判断是否登录成功及登录态是否仍然有效。

**注意：使用高阶方法@cache_name('TemplateLogin')可避免重复实例化**

## 安装与使用

1. 开发完后使用命令`sunday_install login-template`安装该插件
2. 其它地方导入该插件：`from sunday.login.template import getLoginHandler`
3. 执行登录并返回实例化对象: `loginer = getLoginHandler('TemplateLogin')(phone=self.mobile, password=self.password).login()`
4. 使用会话句炳：`loginer.rs.get_json('https://target.site')`

## 参考已有项目

点击下面项目名称查看，或者点击[PySunday login](https://github.com/orgs/pysunday-plugins/repositories?q=login)查看其它登录插件

1. [税务局登录](https://github.com/pysunday-plugins/login-etax)
2. [BOSS直聘登录](https://github.com/pysunday-plugins/login-zhipin)
3. [探迹登录](https://github.com/pysunday-plugins/login-tungee)
