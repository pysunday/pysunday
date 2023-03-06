import os
from sunday.core.globalvar import getvar, setvar
from sunday.core.globalKeyMaps import sdvar_logger, sdvar_exception
from sunday.core.paths import sundayCwd
from sunday.core.cmdexec import cmdexec

def grenKey(num1=None, num2=None):
    """
    生成指定位数标识码, 如grenKey(16, 61)则生成16位字符码来源前61的随机字符串

    标识码字符来源：0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz

    **Parameters:**

    * **num1:** `int` -- 标识码位数
    * **num2:** `int` -- 标识码标识范围
    """
    import random
    words = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    num2 = num2 or len(words)
    ans = [None] * (num1 if num1 is not None else 36)
    a = None
    if num1:
        for n in range(num1):
            ans[n] = words[int(random.random() * num2)]
    else:
        ans[8] = ans[13] = ans[18] = ans[23] = '-'
        ans[14] = '4'
        for n in range(36):
            if not ans[n]: a = int(16 * random.random())
            ans[n] = words[3 & a | 8 if n == 19 else a]
    return ''.join(ans)

def str2base16(oristr):
    """
    字符串转化为十六进制数字串

    **Usage:**
    ```
    >>> from sunday.utils.cryptanalyst import str2base16
    >>> print(str2base16('helloworld'))
    68656c6c6f776f726c64
    ```

    **Parameters:**

    * **oristr:** `str` -- 字符串
    """
    # 字符串转16进制
    return ''.join([hex(ord(s)).replace('0x', '') for s in list(oristr)])

def cryptBySm2(datastrList, key, cryptType='encrypt'):
    """
    国密SM2加解密(非对称加密)

    **Parameters:**

    * **datastrList:** `list` -- 明文或者密闻组成的数组，如一次加密多个密码
    * **key:** `str` -- 加密传公钥, 解密传私钥
    * **cryptType:** `str` -- encrypt(加密)、decrypt(解密)
    """
    if not datastrList: return []
    if type(datastrList) == str:
        datastrList = [datastrList]
    execPath = os.path.join(sundayCwd, 'utils', 'cryptanalysis', f'{cryptType}_sm2.js')
    if not os.path.exists(execPath):
        raise getvar(sdvar_exception)(-1, f'{cryptType}暂不支持，解析文件不存在：{execPath}')
    cmd = 'node {execPath} {key} {cipherMode} {datastr}'.format(
            execPath=execPath,
            key=key,
            cipherMode='1',
            datastr=' '.join(datastrList))
    execcode, stdout, stderr = cmdexec(cmd)
    if execcode != 0:
        getvar(sdvar_logger).error(stderr)
        raise getvar(sdvar_exception)(-1, f'sm2 {cryptType} fail')
    return stdout.strip().split('\n')

def cryptBySm4(datastrList, key, cryptType='encrypt'):
    """
    国密SM4加解密(对称加密)

    **Parameters:**

    * **datastrList:** `list` -- 明文或者密闻组成的数组，如一次加密多个密码
    * **key:** `str` -- 公钥
    * **cryptType:** `str` -- encrypt(加密)、decrypt(解密)
    """
    if not datastrList: return []
    if type(datastrList) == str:
        datastrList = [datastrList]
    execPath = os.path.join(sundayCwd, 'utils', 'cryptanalysis', f'{cryptType}_sm4.js')
    if not os.path.exists(execPath):
        raise getvar(sdvar_exception)(-1, f'{cryptType}暂不支持，解析文件不存在：{execPath}')
    cmd = "node {execPath} {key} {datastr}".format(
            execPath=execPath,
            key=key,
            datastr=' '.join(datastrList))
    execcode, stdout, stderr = cmdexec(cmd)
    if execcode != 0:
        getvar(sdvar_logger).error(stderr)
        raise getvar(sdvar_exception)(-1, f'sm4 {cryptType} fail')
    return stdout.strip().split('\n')

def cryptByJsEncrypt(datastrList, key, cryptType='encrypt', isHex=False):
    """
    jsencrypt加解密

    **Parameters:**

    * **datastrList:** `list` -- 明文或者密闻组成的数组，如一次加密多个密码
    * **key:** `str` -- 公钥
    * **cryptType:** `str` -- encrypt(加密)、decrypt(解密)
    """
    if not datastrList: return []
    if type(datastrList) == str:
        datastrList = [datastrList]
    execPath = os.path.join(sundayCwd, 'utils', 'cryptanalysis', f'{cryptType}_jsencrypt{"_hex" if isHex else ""}.js')
    if not os.path.exists(execPath):
        raise getvar(sdvar_exception)(-1, f'{cryptType}暂不支持，解析文件不存在：{execPath}')
    cmd = 'node {execPath} {key} {datastr}'.format(
            execPath=execPath,
            key=key,
            datastr=' '.join(datastrList))
    execcode, stdout, stderr = cmdexec(cmd)
    if execcode != 0:
        getvar(sdvar_logger).error(stderr)
        raise getvar(sdvar_exception)(-1, f'jsencrypt {cryptType} fail')
    return stdout.strip().split('\n')

def cryptByCryptoJS(datastrList, key, cryptType='encrypt', mode='ECB'):
    """
    cryptoJS加解密

    **Parameters:**

    * **datastrList:** `list` -- 明文或者密闻组成的数组，如一次加密多个密码
    * **key:** `str` -- 公钥
    * **cryptType:** `str` -- encrypt(加密)、decrypt(解密)
    * **mode:** `str` -- 加密方式，默认ECB
    """
    if not datastrList: return []
    if type(datastrList) == str: datastrList = [datastrList]
    execPath = os.path.join(sundayCwd, 'utils', 'cryptanalysis', f'{cryptType}_cryptojs_{mode}.js')
    if not os.path.exists(execPath):
        raise getvar(sdvar_exception)(-1, f'{cryptType}暂不支持，解析文件不存在：{execPath}')
    cmd = 'node {execPath} {key} {datastr}'.format(
            execPath=execPath,
            key=key,
            datastr=' '.join(datastrList))
    execcode, stdout, stderr = cmdexec(cmd)
    if execcode != 0:
        getvar(sdvar_logger).error(stderr)
        raise getvar(sdvar_exception)(-1, f'cryptojs {cryptType} {mode} fail')
    return stdout.strip().split('\n')

def cryptByUuid(datastrList, key, cryptType='decrypt'):
    """
    根据密文与密钥解码出UUID值

    **Parameters:**

    * **datastrList:** `list` -- 明文或者密闻组成的数组，如一次加密多个密码
    * **key:** `str` -- 密钥
    * **cryptType:** `str` -- encrypt(加密)、decrypt(解密)
    """
    if not datastrList: return []
    if type(datastrList) == str:
        datastrList = [datastrList]
    execPath = os.path.join(sundayCwd, 'utils', 'cryptanalysis', f'{cryptType}_aestoolsnsrd.js')
    if not os.path.exists(execPath):
        raise getvar(sdvar_exception)(-1, f'{cryptType}暂不支持，解析文件不存在：{execPath}')
    cmd = "node {execPath} {key} {datastr}".format(
            execPath=execPath,
            key=key,
            datastr=' '.join(datastrList))
    execcode, stdout, stderr = cmdexec(cmd)
    if execcode != 0:
        getvar(sdvar_logger).error(stderr)
        raise getvar(sdvar_exception)(-1, f'aesToolsNsrd decrypt UUID {cryptType} fail')
    return stdout.strip().split('\n')

if __name__ == "__main__":
    key = grenKey(16, 61)
    print(f'========》grenKey(16, 61): {key}')
    print(f'========》str2base16("{key}"): {str2base16(key)}')
    publicKey = '596b71524573654d366b627244346b65'
    origin = '{"a":"haha"}'
    target = cryptBySm4(origin, publicKey, 'encrypt')
    print(f"========》cryptBySm4('{origin}', '{publicKey}', 'decrypt'): {target}")
    print(f"========》cryptBySm4('{target}', '{publicKey}', 'decrypt'): {cryptBySm4(target, publicKey, 'decrypt')}")
    # print(f"cryptBySm2({key}, 'howduudu'): {cryptBySm2(key, 'howduudu')}")
    # print(f"cryptByJsEncrypt({key}, 'howduudu', 'encrypt'): {cryptBySm4(key, 'howduudu', 'encrypt')}")
