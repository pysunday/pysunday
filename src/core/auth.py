# coding: utf-8
import os
from getpass import getpass
from sunday.core.logger import Logger
from sunday.core.getEnv import getEnv
from sunday.core.getConfig import getConfig
from sunday.core.aesCbc import aesCbcDecrypt, aesCbcEncrypt

__all__ = ['getCurrentUser', 'Auth']

logger = Logger('AUTH').getLogger()

def getCurrentUser():
    return getEnv('USER')

cryptoKey = getConfig('CRYPTO')('key')

class Auth():
    """ 用于用户账户认证相关操作
    attributes:
        addParams: 用户名密码等交互元素录入
        getParams: 返回交互结果对象
    examples:
        from utils.auth import Auth
        auth = Auth('path/to/.env')
        auth.addParams('USER')
        auth.addParams('USER', 'ask text', defaultValue="xxx")
        auth.addParams('USER', 'ask text', 'myName')
        auth.addParams('code', isSave=False)
        params = auth.getParams()
    raises:
        请输入env文件路径: 实例化时envPath必传
    """
    def __init__(self, envPath = '', name = ''):
        if not envPath: raise Exception('请输入env文件路径')
        self.name = name
        self.envPath = envPath
        self.tip = {}
        self.val = {}

    def tipMap(self, key):
        tip = key
        if key in ['USER', 'user', 'username', 'USERNAME', 'name', 'NAME']:
            tip = '请输入用户名'
        elif key in ['PWD', 'pwd', 'PASSWORD', 'password']:
            tip = '请输入密码'
        elif key in ['CODE', 'code']:
            tip = '请输入验证码'
        return self.name + tip

    def addParams(self, key, tip = '', value='', defaultValue='', isMust=True, isSave=True, isPass=False):
        """ 用户名密码等交互元素录入
        Args:
            key: 交互元素键名
            tip: 交互时的提示文本
            value: 值存在则跳过交互
            defaultValue: 默认值, 当输入为空时取默认值
            isMust: 是否必填
            isSave: 是否缓存, 用户名密码一般需要缓存, 验证码一般不需要缓存
        Returns:
            value存在则返回value否则返回用户交互结果
        """
        self.tip[key] = self.tipMap(tip or key)
        tarVal = value
        if not value:
            tarVal = self.ask(key, defaultValue, isMust, isSave, isPass)
        elif isPass:
            tarVal = aesCbcDecrypt(value, cryptoKey)
        self.val[key] = tarVal
        return self.val[key]

    def ask(self, key, defaultValue, isMust, isSave, isPass):
        tip = '%s%s: ' % (self.tip[key], '(%s)' % defaultValue if defaultValue else '')
        value = getpass(tip) if isPass else input(tip)
        if value == '':
            if defaultValue:
                value = defaultValue
            elif isMust:
                print('必填项不能为空!')
                return self.ask(key, defaultValue, isMust, isSave)
        if isSave:
            # isPass则存储密文, 否则存储明文
            tarVal = aesCbcEncrypt(value, cryptoKey) if isPass else value
            cmd = 'echo %s=%s >> %s' % (key, tarVal, self.envPath)
            os.system(cmd)
        return value

    def getParams(self):
        return self.val


if __name__ == '__main__':
    auth = Auth()
    auth.addParams('user', '哈哈')

