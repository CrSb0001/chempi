'''
General utils and exceptions
'''

from functools import wraps

from .. import __url__
from .deprecation import Deprecation

def identity(x):
    '''
    The identity function.

    Examples
    ==========
    >>> identity(-5)
    -5
    >>> identity(6)
    6
    '''
    return x

class NoConvergence(Exception):
    pass

class ChemPiDeprecationWarning(DeprecationWarning):
    pass

def deprecated(*args, **kwargs):
    '''
    Helper to :class: `Deprecation` for using ChemPiDeprecationWarning.
    '''
    return Deprecation(*args, issues_url = lambda s: __url__ + '/issues/' + s.strip('gh-'), warning = ChemPiDeprecationWarning, **kwargs)

def memoize(max_nargs = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            if max_nargs is not None and len(args) > max_nargs:
                raise ValueError('Memoization error.')
            
            if args not in wrapper.results:
                wrapper.results[args] = func(*args)
            
            return wrapper.results[args]
        
        wrapper.results = {}
        return wrapper
    
    return decorator
