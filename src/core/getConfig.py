# coding: utf-8
import os
import sunday.core.paths as paths
from configparser import ConfigParser

__all__ = ['getConfig']

defaultConfig = {
    'LOGGING.level': 'ERROR',
    'LOGGING.print_file': False,
    'LOGIN.cookieFile': '.cookies',
    'LOGIN.envFile': '.env',
    # 密钥
    'CRYPTO.key': 'HOWDUUDU'
}

def getConfig(name, file='config.ini', default={}):
    """
    返回能够获取全局配置文件(`$SUNDAY_ROOT/config.ini`)内配置值的函数

    **Parameters:**

    * **name:** `str` -- 键名
    * **file:** `str` -- 文件名
    * **default:** `dict` -- 默认配置的集合，优先级大于全局的配置

    **Return:** `getval(key)`
    """
    configPwd = os.path.join(paths.rootCwd, file)
    cfg = ConfigParser()
    cfg.read(configPwd, encoding='utf-8')
    def getval(key):
        if cfg.has_option(name, key):
            ans = cfg.get(name, key)
            if ans in ['True', 'False']: ans = eval(ans)
            return ans;
        return default.get(key) or defaultConfig.get('.'.join([name, key]))
    return getval

if __name__ == "__main__":
    ans = getConfig('LOGGING')('print_file')
    print(ans)
    print(type(ans))
