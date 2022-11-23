from sunday.core.globalvar import getvar, setvar
from sunday.core.globalKeyMaps import sdvar_exception

class SundayError(Exception): pass

def getException(errorMap={}):
    class CustomError(SundayError):
        def __init__(self, code=10000, message=None, other='', errorMap=errorMap):
            self.code = code
            tip = message or errorMap.get(code, '未知code: %s' % code)
            self.message = tip + ('(%s)' % other if other else '')

        def __str__(self):
            return repr('%d (%s)' % (self.code, self.message))
    return CustomError

if not getvar(sdvar_exception):
    setvar(sdvar_exception, getException())
