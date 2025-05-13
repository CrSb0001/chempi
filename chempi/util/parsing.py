from collections import defaultdict

import re

from .pyutil   import memoize
from .periodic import symbols

_GREEK_LETTERS = (
    'alpha',
    'beta',
    'gamma',
    'delta',
    'epsilon',
    'zeta',
    'eta',
    'theta',
    'iota',
    'kappa',
    'lambda',
    'mu',
    'nu',
    'xi',
    'omicron',
    'pi',
    'rho',
    'sigma',
    'tau',
    'upsilon',
    'phi',
    'chi',
    'psi',
    'omega'
)
_GREEK_UNICODE = 'αβγδεζηθικλμνξοπρστυφχψω'

_LATEX_MAPPING             = {k + '-': '\\' + k + '-' for k in _GREEK_LETTERS}
_LATEX_MAPPING['epsilon-'] = '\\varepsilon'
_LATEX_MAPPING['omicron-'] = 'o-'
_LATEX_MAPPING['.']        = '^\\bullet '
_LATEX_INFIX_MAPPING       = {'..': '\\cdot '}

_UNICODE_MAPPING       = {k + '-': v + '-' for k, v in zip(_GREEK_LETTERS, _GREEK_UNICODE)}
_UNICODE_MAPPING['.']  = '⋅'
_UNICODE_INFIX_MAPPING = {'..': '\u00b7'} # \u00b7: '·'

_HTML_MAPPING       = {k + '-': '&' + k + ';-' for k in _GREEK_LETTERS}
_HTML_MAPPING['.']  = '&sdot;'
_HTML_INFIX_MAPPING = {'..': '&sdot;'}

_UNICODE_SUBSCRIPTS   = {'.': '.'}
_UNICODE_SUPERSCRIPTS = {'+': '⁺', '-': '⁻'}

for k, v in enumerate('₀₁₂₃₄₅₆₇₈₉.'):
    _UNICODE_SUBSCRIPTS[str(k)] = v

for k, v in enumerate('⁰¹²³⁴⁵⁶⁷⁸⁹'):
    _UNICODE_SUPERSCRIPTS[str(k)] = v

def _get_leading_integer(string):
    matches_ = re.findall(r'^\d+', string)
    if len(matches_) == 0:
        matches_ = 1
    
    elif len(matches_) == 1:
        string   = string[len(m[0]):]
        matches_ = int(_matches[0])
    
    else:
        raise ValueError('Failed to parse %s.' % string)
    
    return matches_, string
