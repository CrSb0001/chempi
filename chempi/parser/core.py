'''
Helper utilities for parsing chemical formulas.
'''
from __future__ import annotations # For sys.version < (3, 11, 0)

from abc       import ABC, abstractmethod
from collections import deque
from enum      import Enum
from functools import cached_property

from typing import (
    Any, Callable, Generator, NamedTuple, Optional, Sequence, TextIO, Union)

import copy
# import re
import sys
# ...

from .results import ParseResults, _ParseResultsWithOffset


class __config_flags(ABC):
    pass

class __compat__(__config_flags):
    '''
    A cross-version compatibility config for parser features
    that will be released in the future.
    
    By setting values in ``__compat__`` to True, these features can be
    enabled in previous releases for compatibility testing.
    '''
    _type_desc = 'compatibility'
    
    collect_and_All_tokens = True
    
    _all_names = [__ for __ in locals() if not __.startswith('_')]
    _fixed_names = '''
        collect_and_All_tokens
        '''.split()

class __diag__(__config_flags): # type: ignore
    '''
    Helper for the Diagnostics class
    '''
    _type_desc = 'diagnostic'
    
    warn_multiple_tokens_in_named_alternation = False
    warn_ungrouped_named_tokens_in_collection = False
    warn_name_set_on_empty_FORWARD            = False
    warn_on_parse_using_empty_FORWARD         = False
    warn_on_assignment_to_FORWARD             = False
    warn_on_multiple_string_args_to_oneof     = False
    warn_on_match_first_with_lshift_operator  = False
    enable_debug_on_named_expressions         = False
    
    _all_names   = [__ for __ in locals() if not __.startswith('_')]
    _warn_names  = [name for name in _all_names if name.startswith('_')]
    _debug_names = [name for name in _all_names if name.startswith('enable_debug')]
    
    @classmethod
    def disable(cls, warning) -> None:
        setattr(cls, warning, False)

    @classmethod
    def enable(cls, warning) -> None:
        setattr(cls, warning, True)

    @classmethod
    def enable_all_warnings(cls) -> None:
        for name in cls._warn_names:
            cls.enable(name)

class Diagnostics(Enum):
    '''
    Diagnostic configuration (by default all set to disabled).
    
    - `warn_multiple_tokens_in_named_alternation`: Flag to enable warning when a result's name
        is named on a :class: `MatchFirst` or :class: `Or` expression with one or more :class: `And` subexpressions.
    - `warn_ungrouped_named_tokens_in_collection`:
    - `warn_name_set_on_empty_FORWARD`:
    - `warn_on_parse_using_empty_FORWARD`:
    - `warn_on_assignment_to_FORWARD`:
    - `warn_on_multiple_string_args_to_oneof`:
    - `enable_debug_on_named_expressions`: Flag to auto-enable all subsequent calls to :class: `ParserElement.set_name`
    '''
    warn_multiple_tokens_in_named_alternation = 0
    warn_ungrouped_named_tokens_in_collection = 1
    warn_name_set_on_empty_FORWARD            = 2
    warn_on_parse_using_empty_FORWARD         = 3
    warn_on_assignment_to_FORWARD             = 4
    warn_on_multiple_string_args_to_oneof     = 5
    warn_on_match_first_with_lshift_operator  = 6
    enable_debug_on_named_expressions         = 7

def enable_diag(diag_enum: Diagnostics) -> None:
    __diag__.enable(diag_enum.name)

def disable_diag(diag_enum: Diagnostics) -> None:
    __diag__.disable(diag_enum.name)

def enable_all_warnings() -> None:
    __diag__.enable_all_warnings()

# Hide abstract class so it cannot be accidentally accessed.
del __config_flags

_single_arg_builtins = {
    all, any, len, list, max, min, reversed, set, sorted, sum, tuple
}

_MAX_INT = sys.maxsize
str_type: tuple[type, ...] = (str, bytes)

ParseImplReturnType = tuple[int, Any]
PostParseReturnType = Union[ParseResults, Sequence[ParseResults]]

ParseCondition = Union[Callable[[], bool], Callable[[ParseResults], bool], Callable[[int, ParseResults], bool], Callable[[str, int, ParseResults], bool]]
ParseAction = Callable[[None]]
ParseFailAction = Callable[[str, int, 'ParserElement', Exception], None]

DebugStartAction = Callable[[str, int, 'ParserElement', bool], None]
DebugSuccessAction = Callable[[str, int, int, 'ParserElement', Exception, bool], None]
DebugExceptionAction = Callable[[str, int, 'ParserElement', Exception, bool], None]

class _ParseActionIndexError(Exception):
    '''
    Internal wrapper for IndexError so that IndexErrors raised inside
    actions related to parsing aren't misinterpreted as IndexErrors
    raised inside ParserElement parse_impl methods.
    '''
    def __init__(self, msg: str, exc: BaseException) -> None:
        self.msg: str = msg
        self.exc: BaseException = exc

class ParserElement(ABC):
    DEFAULT_WHITE_CHARS: str = '\x09\x0a\x0d\x20'
    VERBOSE_STACKTRASE: bool = False
    _literal_string_class: type | None = None
    
    @staticmethod
    def set_def_whitespace_chars(chars: str) -> None:
        '''Method to override the set DEFAULT_WHITE_CHARS, which are [\x09, \x0a, \x0d, \x20].'''
        ParserElement.DEFAULT_WHITE_CHARS = chars
        
        # Update default whitespace for all parser expressions defined in the module.
        for expr in _builtin_exprs: # type: ignore
            if expr.copy_default_white_chars:
                expr.white_chars = set(chars)
    
    @classmethod
    def inline_literals_using(cls: type) -> None:
        ParserElement._literal_string_class = cls
    
    @classmethod
    def using_each(cls, seq, **class_kwargs):
        yield from (cls(obj, **class_kwargs) for obj in seq)
    
    class DebugActions(NamedTuple):
        debug_try: Optional[DebugStartAction]
        debug_match: Optional[DebugSuccessAction]
        debug_fail: Optional[DebugExceptionAction]
    
    def __init__(self, savelist: bool = False) -> None:
        self.parse_action: list[ParseAction] = list()
        self.fail_action: Optional[ParseFailAction] = None
        self.custom_name: str | None = None
        self._default_name: Optional[str] = None
        self.results_name: str | None = None
        self.save_as_list: bool = savelist
        self.skip_whitespace: bool = True
        self.white_chars = set(ParserElement.DEFAULT_WHITE_CHARS)
        self.copy_DEFAULT_WHITE_CHARS = True
        self._may_return_empty = True
        self.keep_tabs = False
        self.ignore_exprs: list[ParserElement] = list()
        self.debug: bool = False
        self.streamlined: bool = False
        self.may_index_error: bool = True
        self.errmsg: Union[str, None] = ''
        self.modal_results: bool = True
        self.debug_actions = self.DebugActions(None, None, None)
        self.call_preparse = True
        self.call_during_try = False
        self.suppress_warnings_: list[Diagnostics] = []
        self.show_in_diagram: bool = True
    
    def __iter__(self):
        yield self

    @property
    def may_return_empty(self):
        return self._may_return_empty
    
    @may_return_empty.setter
    def may_return_empty(self, value) -> None:
        self._may_return_empty = value
    
    def suppress_warning(self, warning_type: Diagnostics) -> ParserElement:
        '''
        Suppress warnings emitted from a particular diagnostic
        '''
        self.suppress_warnings_.append(warning_type)
        return self
    
    def visit_all(self) -> Generator:
        to_visit = deque([self])
        seen = set()
        while to_visit:
            cur = to_visit.popleft()
            
            # Guard looping forever through recursive grammars
            # to catch possible unforseen exceptions
            if cur in seen:
                continue
            
            seen.add(cur)
            
            to_visit.extend(cur.recurse())
            yield cur
    
    def copy(self) -> ParserElement:
        '''
        Makes a copy of this :class: `ParserElement`. This is useful for
        defining different parse actions for the same parsing pattern.
        
        The aforementioned action will use copies of the original parse element.
        '''
        copy_ = copy.copy(self)
        copy_.parse_action = self.parse_action[:]
        copy_.ignore_exprs = self.ignore_exprs[:]
        
        if self.copy_DEFAULT_WHITE_CHARS:
            copy_.white_chars = set(ParserElement.DEFAULT_WHITE_CHARS)
        
        return copy_

    def recurse(self):
        return self