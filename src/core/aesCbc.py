import base64
from Crypto.Cipher import AES
from Crypto import Random
from hashlib import md5

__all__ = ['aesCbcDecrypt', 'aesCbcEncrypt']

def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16).encode()

def unpad(s):
    return s[0:-ord(s[len(s)-1:])]

def bytes_to_key(data, salt, output=48):
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]

def aesCbcEncrypt(data, passphrase):
    if type(data) == str: data = data.encode()
    if type(passphrase) == str: passphrase = passphrase.encode()
    salt = Random.new().read(8)
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    cipherbyte = base64.b64encode(b"Salted__" + salt + aes.encrypt(pad(data)))
    return cipherbyte.decode()

def aesCbcDecrypt(data, passphrase):
    if type(data) == str: data = data.encode()
    if type(passphrase) == str: passphrase = passphrase.encode()
    data = base64.b64decode(data)
    assert data[:8] == b'Salted__'
    salt = data[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    plainbyte = unpad(aes.decrypt(data[16:]))
    return plainbyte.decode()

if __name__ == '__main__':
    data = b'8879576hdud'
    passphrase = b'HOWDUUDU'

    encrypt_data = aesCbcEncrypt(data, passphrase)
    print('encrypt_data:', encrypt_data)

    encrypt_data = b"U2FsdGVkX1+N4vlBhSYzxlN075knzFQk4l4VsxT71h0="

    decrypt_data = aesCbcDecrypt(encrypt_data, passphrase)
    print('decrypt_data:', decrypt_data)

