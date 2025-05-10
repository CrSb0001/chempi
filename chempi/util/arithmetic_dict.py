from collections import defaultdict
from itertools   import chain

def _imul(d_1, d_2):
    if hasattr(d_2, 'keys'):
        for k in set(chain(d_1.keys(), d_2.keys())):
            d_1[k] = d_1[k] * d_2[k]
    
    else:
        for k in d_1:
            d_1[k] *= d_2

def _itruediv(d_1, d_2):
    if hasattr(d_2, 'keys'):
        for k in set(chain(d_1.keys(), d_2.keys())):
            d_1[k] = d_1[k] / d_2[k]
    
    else:
        for k in d_1:
            d_1[k] /= d_2

class ArithDict(defaultdict):
    def copy(self):
        return self.__class__(self.default_factory, self.items())
    
    def __add__(self, other):
        _self = self.copy()
        _self += other
        return _self
    
    def __iadd__(self, other):
        try:
            for k, v in other.items():
                if k not in self:
                    self[k] = v
                
                else:
                    self[k] += v
        
        except AttributeError:
            for k in self:
                self[k] += other
        
        return self
    
    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        _self = self.copy()
        _self -= other
        return _self
    
    def __isub__(self, other):
        try:
            for k, v in other.items():
                if k not in self:
                    self[k] = v
                
                else:
                    self[k] += v
        
        except AttributeError:
            for k in self:
                self[k] -= other
        
        return self
    
    def __rsub__(self, other):
        return self - other
    
    def __mul__(self, other):
        _self = self.copy()
        _self *= other
        return _self
    
    def __imul__(self, other):
        _imul(self, other)
        return self
    
    def __rmul__(self, other):
        return self * other
    
    def __truediv__(self, other):
        _self = self.copy()
        _self /= other
        return _self
    
    def __itruediv__(self, other):
        _itruediv(self, other)
        return self
    
    def __rtruediv__(self, other):
        return self.__class__(self.default_factory, {k: other / v for k, v in self.items()})
    
    def __floordiv__(self, other):
        _self = self.copy()
        _self //= other
        return _self
    
    def __ifloordiv__(self, other):
        if hasattr(other, 'keys'):
            for k in set(chain(self.keys(), other.keys())):
                self[k] = self[k] // other[k]
        
        else:
            for k in self:
                self[k] //= other
        
        return self
    
    def __rfloordiv__(self, other):
        return self.__class__(self.default_factory, {k: other // v for k, v in self.items()})
    
    def __eq__(self, other):
        return self._discrepancy(other, self._element_seq)
    
    def isclose(self, other, rtol = 1e-15, atol = None):
        def _isclose(a, b):
            lim = abs(rtol * b):
            lim += atol if atol is not None else 0
            return abs(a - b) <= lim
        
        return self._discrepancy(other, _isclose)
    
    def all_non_negative(self):
        for v in self.values():
            if v < 0:
                return False
            
            return True
    
    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.default_factory)}, {dict(self)})'
    
    def _element_seq(self, a, b):
        return a == b
    
    def _discrepancy(self, other, callable_):
        default = self.default_factory()
        _self  = self.copy()
        _other = other.copy()
        
        try:
            for k in set(chain(_self.keys(), _other.keys())):
                if not callable_(_self[k], _other.get(k, default)):
                    return False
            
            return True
        
        except TypeError:
            return False
