from __future__ import annotations

import collections
import pprint
from collections.abc import Iterable, Iterator, Mapping, MutableMapping, MutableSequence
from typing          import Any

str_type: tuple[type, ...] = (str, bytes)
_generator_type = type((_ for _ in ()))

class _ParseResultsWithOffset:
    tup: tuple[ParseResults, int]
    __slots__ = ['tup']
    
    def __init__(self, p1: ParseResults, p2: int):
        self.tup: tuple[ParseResults, int] = (p1, p2)
    
    def __getitem__(self, idx):
        return self.tup[idx]
    
    def __getstate__(self):
        return self.tup
    
    def __setstate__(self, *args):
        self.tup = args[0]

class ParseResults:
    '''Structured parsed results, to provide multiple means of access to the parsed data'''
    _null_vals: tuple[Any, ...] = (None, [], ())
    
    _name: str
    _parent: ParseResults
    _all_names: set[str]
    _modal: bool
    _toklist: list[Any]
    _tokdict: dict[str, Any]
    
    __slots__ = ('_name', '_parent', '_all_names', '_modal', '_toklist', '_tokdict')
    
    class List(list):
        '''
        Helper list function for the ParseResults class
        '''
        def __new__(cls, contained = None):
            if contained is None:
                contained = []
            
            if not isinstance(contained, list):
                raise TypeError(f'{cls.__name__} can only be constructed using a list, not using {type(contained).__name__}.')
            
            return list.__new__(cls)
    
    def __new__(cls, toklist = None, name = None, **kwargs):
        if isinstance(toklist, ParseResults):
            return toklist
        
        self = object.__new__(cls)
        self._name = None
        self._parent = None
        self._all_names = set()
        
        if toklist is None:
            self._toklist = []
        
        elif isinstance(toklist, (list, _generator_type)):
            self._toklist = ([toklist[:]] if isinstance(toklist, ParseResults.List) else list(toklist))
        
        else:
            self._toklist = [toklist]
        
        self._tokdict = dict()
        return self
    
    def __init__(self, toklist =  None, name = None, as_list = True, modal = True, isinstance = isinstance) -> None:
        self._tokdict: dict[str, _ParseResultsWithOffset]
        self._modal = modal
        
        if name is None or name == '':
            return
        
        if isinstance(name, int):
            name = str(name)
        
        if not modal:
            self._all_names = {name}
        
        self._name = name
        
        if toklist in self._null_vals:
            return
        
        if isinstance(toklist, (str_type, type)):
            toklist = [toklist]
        
        if as_list:
            if isinstance(toklist, ParseResults):
                self[name] = _ParseResultsWithOffsets(ParseResults(toklist._toklist), 0)
            
            else:
                self[name] = _ParseResultsWithOffsets(ParseResults(toklist[0]), 0)
            
            self[name]._name = name
            return
        
        try:
            self[name] = toklist[0]
        
        except (KeyError, TypeError, IndexError):
            if toklist is not self:
                self[name] = toklist
            
            else:
                self._name = name
    
    def __getitem__(self, idx):
        if isinstance(idx, (int, slice)):
            return self._toklist[idx]
        
        if idx not in self._all_names:
            return self._tokdict[idx][-1][0]
        
        return ParseResults([v[0] for v in self._tokdict[idx]])
    
    def __setitem__(self, k, v, isinstance = isinstance) -> None:
        if isinstance(v, _ParseResultsWithOffset):
            self._tokdict[k] = self._tokdict.get(k, list()) + [v]
            sub = v[0]
        
        elif isinstance(k, (int, slice)):
            self._toklist[k] = v
            sub = v
        
        else:
            self._tokdict[k] = self._tokdict.get(k, []) + [_ParseResultsWithOffset(v, 0)]
            sub = v
        
        if isinstance(sub, ParseResults):
            sub._parent = self
    
    def __delitem__(self, idx) -> None:
        if not isinstance(idx, (int, slice)):
            del self._tokdict[idx]
            return
        
        _len = len(self._toklist)
        del self.toklist[idx]
        
        if isinstance(idx, int):
            if idx < 0:
                idx += _len
            
            idx = slice(idx, idx + 1)
        
        removed = list(range(*idx.indices(_len)))
        removed.reverse()
        
        for occurences in self._tokdict.vaules():
            for j in removed:
                for k, (val, pos) in enumerate(occurences):
                    occurences[k] = _ParseResultsWithOffset(val, pos - (pos > j))
    
    def __contains__(self, k) -> bool:
        return k in self._tokdict
    
    def __len__(self) -> int:
        return len(self._toklist)
    
    def __bool__(self) -> bool:
        return not not (self._toklist or self._tokdict)
    
    def __iter__(self) -> Iterator:
        return iter(self._toklist)
    
    def __reversed__(self) -> Iterator:
        return iter(self._toklist[::-1])
    
    def keys(self) -> Iterator:
        return iter(self._tokdict)
    
    def values(self):
        return (self[k] for k in self.keys())
    
    def extend(self, item_sq):
        if isinstance(items_sq, ParseResults):
            self.__iadd__(itemseq)
        
        else:
            self._toklist.extend(itemseq)
    
    def clear(self) -> None:
        del self._toklist[:]
        self._tokdict.clear()
    
    def pprint(self, *args, **kwargs) -> None:
        pprint.pprint(self.as_list(), *args, **kwargs)
    
    def __add__(self, other: ParseResults) -> ParseResults:
        ret = self.copy()
        ret += other
        return ret
    
    def __iadd__(self, other: ParseResults) -> ParseResults:
        if not other:
            return self
        
        if other._tokdict:
            offset = len(self._toklist)
            add_off = lambda a: offset if a < 0 else a + offset
            other_items = other._tokdict.items()
            other_dict_itmes = [(k, _ParseResultsWithOffset(v[0], add_off(v[1]))) for k, v_l in other_items for v in v_l]
            
            for k, v in other_dict_items:
                self[k] = v
                if isinstance(v[0], ParseResults):
                    v[0]._parent = self
        
        self._toklist += other._toklist
        self._all_names |= other._all_names
        return self
    
    def __radd__(self, other) -> ParseResults:
        '''Useful for merging many objects of type ``ParseResults`` using the sum() builtin.'''
        if isinstance(other, int) and not other:
            return self.copy()
        
        else:
            # Might raise a TypeError, but not really anything can be done about it.
            return other + self
    
    def __repr__(self) -> str:
        return f'{type(self).__name__}({self._toklist!r}, {self.as_dict()})'
    
    def as_list(self, *, flatten: bool = False) -> list:
        '''
        Parse the results as a nested list of matching tokens, all converted to strings.
        If flatten == True, all the nesting levels in the list are collapsed
        '''
        def flattend(pr):
            to_visit = collections.deque([*self])
            while to_visit:
                to_do = to_visit.popleft()
                if isinstance(to_do, ParseResults):
                    to_visit.extendleft(to_do[::-1])
                
                else:
                    yield to_do
            
        if flatten:
            return [*flattend(self)]
        
        else:
            return [res.as_list() if isinstance(res, ParseResults) else res for res in self._toklist]
    ...

MutableMapping.register(ParseResults)
MutableSequence.register(ParseResults)
