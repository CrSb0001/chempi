from functools import reduce
from operator  import add, mul

'''
If Python 2 support is really required, then we at the very least don't want
any issues of more time spent importing chempi by determining if there's an
ImportError.

However, note that ChemPi is not intended to actually support Python 2, only
Python 3.
'''

def _any(arg):
    if arg is True:
        return True
    
    if arg is False:
        return False
    
    return any(arg)

def prodpow(bases, exponents):
    res = []
    for row in exponents:
        _ = 1
        for base, exponent in zip(bases, row):
            _ *= base ** exponent
        
        res.append(_)
    
    return res

def get_backend(backend):
    if isinstance(backend, str):
        backend = __import__(backend)
    
    if backend is None:
        import numpy as backend
    
    return backend

def int_div(p, q):
    '''
    Integer division that rounds towards 0, like the first arg
    in Python's builtin divmod.
    '''
    r = p // q
    if r < 0 and q * r != p:
        r += 1
    
    return r

def reducemap(args, reduce_op, map_op):
    return reduce(reduce_op, map(map_op, *args))

def vec_dot(vec_1, vec_2):
    return reducemap((vec_1, vec_2), add, mul)

def mat_dot_vec(iter_mat, iter_vec, iter_term = None):
    if iter_term is None:
        return [vec_dot(row, iter_vec) for row in iter_mat]
    
    else:
        return [vec_dot(row, iter_vec) + term for row, term in zip(iter_mat, iter_term)]

def coerce(obj1, obj2):
    return obj1.__coerce__(obj2)