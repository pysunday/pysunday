import hashlib

def getMd5(value):
    """
    文本生成md5值

    **Parameters:**

    * **value:** `str` -- 文本字符串
    """
    md5 = hashlib.md5()
    md5.update(value.encode('utf-8'))
    return md5.hexdigest()
