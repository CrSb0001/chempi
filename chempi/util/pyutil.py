'''
General utils and exceptions
'''

from collections     import defaultdict, namedtuple, OrderedDict
from collections.abc import ItemsView, Mapping
from functools       import wraps
from itertools       import product

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
    '''Helper to :class: `Deprecation` for using ChemPiDeprecationWarning.'''
    return Deprecation(*args, issues_url = lambda s: __url__ + '/issues/' + s.strip('gh-'), warning = ChemPiDeprecationWarning, **kwargs)

class AttrContainer(object):
    '''Class method used to turn e.g. a dict object into a module-like object.'''
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
    
    def as_dict(self):
        return self.__dict__.copy()
    
    def __repr__(self):
        return f'{self.__class__.__name__}({", ".join(set(dir(self)) - set(dir(object())))})'

class AttrDict(object):
    '''Subclass of dict object with attribute access to keys'''
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

class defaultkeydict(defaultdict):
    '''defaultdict where default_factory is intended to have the signature key'''
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(f'Missing key: {key}')
        
        else:
            self[key] = self.default_factory(key)
        
        return self[key]

class DeferredImport(object):
    def __init__(self, modname, arg = None, decorators = None):
        self._modname    = modname
        self._arg        = arg
        self._decorators = decorators
        self._cache      = None
    
    @property
    def cache(self):
        if self._cache is None:
            if self._arg is None:
                obj = __import__(self._modname)
            
            else:
                obj = getattr(__import__(self._modname, globals(), locals(), [self._arg]), self._arg)
            
            if self._decorators is not None:
                for deco in self._decorators:
                    obj = deco(obj)
            
            self._cache = obj
        
        return self._cache
    
    def __getattr__(self, attr):
        if attr in ('_modname', '_arg', '_cache', 'cache', '_decorators'):
            return object.__getattr__(self, attr)
        
        else:
            return getattr(self.cache, attr)
    
    def __call__(self, *args, **kwargs):
        return self.cache(*args, **kwargs)

class NameSpace:
    '''
    Used to wrap, for example, modules.

    The only parameter, `default`, is used as a fallback for attribute access.
    '''
    def __init__(self, default):
        self._NameSpace_default    = default
        self._NameSpace_attr_store = {}
    
    def __getattr__(self, attr):
        if attr.startswith('_NameSpace_'):
            return self.__dict__[attr]
        
        else:
            try:
                return self._NameSpace_attr_store[attr]
            
            except KeyError:
                return getattr(self._NameSpace_default, attr)
    
    def __setattr__(self, attr, val):
        if attr.startswith('_NameSpace_'):
            self.__dict__[attr] = val
        
        else:
            self._NameSpace_attr_store[attr] = val
    
    def as_dict(self):
        items  = self._NameSpace_default.__dict__.items()
        result = {k: v for k, v in items if not k.startswith('_')}
        result.update(self._NameSpace_attr_store)
        return result

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
