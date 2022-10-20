def getException(errorMap={}):
    class SundayError(Exception):
        def __init__(self, code=10000, message=None, other=''):
            self.code = code
            tip = message or errorMap.get(code, '未知code: %s' % code)
            self.message = tip + ('(%s)' % other if other else '')

        def __str__(self):
            return repr('%d (%s)' % (self.code, self.message))
    return SundayError
