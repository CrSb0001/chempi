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
