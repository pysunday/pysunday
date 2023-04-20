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

def cryptBySm4Js(datastrList, key, cryptType='encrypt'):
    if not datastrList: return []
    if type(datastrList) == str:
        datastrList = [datastrList]
    return sm4.call(cryptType, datastrList, key)

if __name__ == "__main__":
    publicKey = '596b71524573654d366b627244346b65'
    origin = '{"a":"haha"}'
    target = cryptBySm4Js(origin, publicKey, 'encrypt')
    print(f"========》cryptBySm4('{origin}', '{publicKey}', 'decrypt'): {target}")
    print(f"========》cryptBySm4('{target}', '{publicKey}', 'decrypt'): {cryptBySm4Js(target, publicKey, 'decrypt')}")
