from functools import wraps
from threading import Thread
"""
Provides two features:
    - A timeout decorator that forces functions to RETURNS a TimeoutError after 1 second
    - A make_timeout decorator making method that lets you specify a time (seconds)
      and a return_value to be returned after that time.
    - An is_timeout function to test a result for being a timeout
"""

DEFAULT_TIME = 1


class TimeoutError(Exception):
    pass


def is_timeout(result):
    return isinstance(result, TimeoutError)


def make_timeout(seconds=DEFAULT_TIME, return_value = TimeoutError()):
    def deco(func):
        def wrapper(*args, **kwargs):
            TIMED_OUT ="timedout"
            res = [TIMED_OUT]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception, e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            t.start()
            t.join(seconds)
            ret = res[0]
            if ret == TIMED_OUT:
                return return_value
            return ret
        return wraps(func)(wrapper)
    return deco

timeout = make_timeout()