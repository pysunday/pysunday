from sunday.core.globalvar import getvar, setvar
from sunday.core.globalKeyMaps import sdvar_logger, sdvar_exception

def grenKey(num1=None, num2=None):
    # 生成指定位数标识码, 如grenKey(16, 61)
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
    # 字符串转16进制
    return ''.join([hex(ord(s)).replace('0x', '') for s in list(oristr)])

def cryptBySm2(datastrList, key, cryptType='encrypt'):
    """
    国密2加解密
    key: encrypt传公钥, decrypt传私钥
    cryptType: encrypt(加密)、decrypt(解密)
    """
    if not datastrList: return []
    if type(datastrList) == str:
        datastrList = [datastrList]
    cmd = 'node {execPath} {key} {cipherMode} {datastr}'.format(
            execPath=os.path.join(self.pwd, 'cryptanalysis', f'{cryptType}_sm2.js'),
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
    国密4加解密
    key: 公钥
    cryptType: encrypt(加密)、decrypt(解密)
    """
    if not datastrList: return []
    if type(datastrList) == str:
        datastrList = [datastrList]
    cmd = "node {execPath} {key} '{datastr}'".format(
            execPath=os.path.join(self.pwd, 'cryptanalysis', f'{cryptType}_sm4.js'),
            key=key,
            datastr=' '.join(datastrList))
    execcode, stdout, stderr = cmdexec(cmd)
    if execcode != 0:
        getvar(sdvar_logger).error(stderr)
        raise getvar(sdvar_exception)(-1, f'sm4 {cryptType} fail')
    return stdout.strip().split('\n')

def cryptByJsEncrypt(datastrList, key, cryptType='encrypt'):
    """
    jsencrypt加解密
    key: 公钥
    cryptType: encrypt(加密)、decrypt(解密)
    """
    if not datastrList: return []
    if type(datastrList) == str:
        datastrList = [datastrList]
    cmd = 'node {execPath} {key} {datastr}'.format(
            execPath=os.path.join(self.pwd, 'cryptanalysis', f'{cryptType}_jsencrypt.js'),
            key=key,
            datastr=' '.join(datastrList))
    execcode, stdout, stderr = cmdexec(cmd)
    if execcode != 0:
        getvar(sdvar_logger).error(stderr)
        raise getvar(sdvar_exception)(-1, f'jsencrypt {cryptType} fail')
    return stdout.strip().split('\n')
