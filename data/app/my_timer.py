# Full disclosure I modified this from code I found on StackOverflow
# https://stackoverflow.com/questions/1622943/timeit-versus-timing-decorator
# https://stackoverflow.com/questions/1148309/how-to-calculate-time-elapsed-in-python
from functools import wraps
from time import time


def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        time_elapsed = te - ts
        if time_elapsed < 60:
            oString = "{} seconds".format(time_elapsed)
        elif time_elapsed < 3600:
            oString = "{} minutes".format(time_elapsed/60)
        else:
            oString = "{} hours".format(time_elapsed/3600)
        print('func:%r args:[%r, %r] took: %r' %
              (f.__name__, args, kw, oString))
        return result
    return wrap