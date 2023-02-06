from sunday.core.globalvar import getvar, setvar
from sunday.core.globalKeyMaps import sdvar_exception
from pydash.objects import pick
from pydash.arrays import union

class SundayError(Exception): pass

def getException(errorMap={}, allowAttr=[]):
    """
    生成报错捕获对象，继承于CustomError > SundayError，默认存在属性code、message

    **Usage:**

    ```
    >>> from sunday.core.getException import getException
    >>> MyError = getException({ 10000: '错误提示文本' })
    >>> raise MyError(10000)
    ```

    **Parameters:**

    * **errorMap:** `dict` -- 错误映射字典，一般就是数字或字符键对应报错说明
    * **allowAttr:** `list` -- 允许的额外属性键列表

    **Return:** `NewError`
    """
    class CustomError(SundayError):
        def __init__(self, code=10001, message=None, other='', errorMap=errorMap, **kwargs):
            self.code = code
            tip = message or errorMap.get(code, '未知code: %s' % code)
            self.message = tip + ('(%s)' % other if other else '')
            kwargs = pick(kwargs, allowAttr) if type(allowAttr) == list and len(allowAttr) > 0 else kwargs
            for key in union([i for i in kwargs.keys()], allowAttr):
                setattr(self, key, kwargs.get(key) or '')

        def __str__(self):
            return repr('%d %s' % (self.code, self.message))

        def __iter__(self):
            iters = dict((x,y) for x, y in self.__dict__.items() if x[:2] != '__')
            iters.update(self.__dict__)
            for x, y in iters.items():
                yield x, y

    return CustomError

if not getvar(sdvar_exception):
    setvar(sdvar_exception, getException())
