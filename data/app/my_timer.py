# Full disclosure I modified this from code I found on StackOverflow
# https://stackoverflow.com/questions/1622943/timeit-versus-timing-decorator
# https://stackoverflow.com/questions/1148309/how-to-calculate-time-elapsed-in-python
from functools import wraps
from time import perf_counter
from my_logger import initTimeAnalysis_logger

# This is a decorator that will time the function it expects at least one argument which could be (self)
tL = initTimeAnalysis_logger()

def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = perf_counter()
        result = f(*args, **kw)
        te = perf_counter()
        time_elapsed = te - ts
        if time_elapsed < 60:
            oString = "{:f} seconds".format(time_elapsed)
        elif time_elapsed < 3600:
            oString = "{:f} minutes".format(time_elapsed/60)
        else:
            oString = "{:f} hours".format(time_elapsed/3600)
        print('func:%r args:[%r, %r] took: %r' %
              (f.__name__, args[1:], kw, oString))
        # if len(args) > 2:
            # tL.info(f"{f.__name__} with {args[2:]} took {oString} seconds")
        if result is not None:     
            return result
        else:
            return time_elapsed
    return wrap