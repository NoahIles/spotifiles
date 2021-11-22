# Full disclosure I modified this from code I found on StackOverflow
# https://stackoverflow.com/questions/1622943/timeit-versus-timing-decorator
# https://stackoverflow.com/questions/1148309/how-to-calculate-time-elapsed-in-python
from functools import wraps
from time import time

# This is a decorator that will time the function it expects at least one argument which could be (self)
def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        time_elapsed = te - ts
        if time_elapsed < 60:
            oString = "{:f} seconds".format(time_elapsed)
        elif time_elapsed < 3600:
            oString = "{:f} minutes".format(time_elapsed/60)
        else:
            oString = "{:f} hours".format(time_elapsed/3600)
        print('func:%r args:[%r, %r] took: %r' %
              (f.__name__, args[1:], kw, oString))
        return result
    return wrap