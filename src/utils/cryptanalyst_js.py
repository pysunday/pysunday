import execjs
import os
from sunday.core.paths import sundayCwd

execPath = os.path.join(sundayCwd, 'utils', 'cryptanalysis')
sm4 = execjs.compile("""
const sm4 = require('%s/sm4.js')

function encrypt(datastrList, publicKey) {
    return datastrList.map(each => sm4.encrypt(each, publicKey))
}

function decrypt(datastrList, publicKey) {
    return datastrList.map(each => sm4.decrypt(each, publicKey))
}
""" % (execPath, ))

crypto = execjs.compile("""
const crypto = require('%s/crypto.js')

function encrypt(datastrList) {
    return datastrList.map(each => crypto.encrypt(each))
}
""" % (execPath, ))

def cryptBySm4Js(datastrList, key, cryptType='encrypt'):
    if not datastrList: return []
    if type(datastrList) == str:
        datastrList = [datastrList]
    return sm4.call(cryptType, datastrList, key)

def cryptByCrypto(datastrList, cryptType='encrypt'):
    # 探迹用的加密
    if not datastrList: return []
    if type(datastrList) == str:
        datastrList = [datastrList]
    return crypto.call(cryptType, datastrList)

if __name__ == "__main__":
    publicKey = '596b71524573654d366b627244346b65'
    origin = '{"a":"haha"}'

    target = cryptBySm4Js(origin, publicKey, 'encrypt')
    print(f"========》cryptBySm4('{origin}', '{publicKey}', 'decrypt'): {target}")
    print(f"========》cryptBySm4('{target}', '{publicKey}', 'decrypt'): {cryptBySm4Js(target, publicKey, 'decrypt')}")

    target = cryptByCrypto(origin, 'encrypt')
    print(f"========》cryptByCrypto('{origin}', 'encrypt'): {target}")
