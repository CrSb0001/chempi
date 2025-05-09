from ._url     import __url__
from ._release import __version__


from .util.pyutil import ChemPiDeprecationWarning

from sys      import version_info
if version_info < (3, 0, 0):
    from warnings import warn
    warn('Some functions might not work due to ChemPi\'s decision to not support Python 2.X.', ChemPiDeprecationWarning)

elif version_info < (3, 5, 0):
    from warnings import warn
    warn('Please consider migrating to a newer version of Python as ChemPi might contain functions that only work starting version Python 3.6+.', ChemPiDeprecationWarning)
