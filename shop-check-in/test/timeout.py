from functools import wraps
from threading import Thread
import signal

class TimeoutError(Exception):
    pass

def make_timeout(seconds):
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, seconds))]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception, e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(seconds)
            except Exception, je:
                print 'error starting thread'
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                return ret
            return ret
        return wrapper
    return deco

timeout = make_timeout(1)