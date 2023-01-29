from sunday.core.globalvar import getvar, setvar
from sunday.core.globalKeyMaps import sdvar_exception
from pydash.objects import pick
from pydash.arrays import union

class SundayError(Exception): pass

def getException(errorMap={}, allowAttr=[]):
    class CustomError(SundayError):
        def __init__(self, code=10000, message=None, other='', errorMap=errorMap, **kwargs):
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
