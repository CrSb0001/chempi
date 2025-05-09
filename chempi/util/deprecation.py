import warnings

class Deprecation(object):
    """Decorator factory for deprecating functions/classes.
	
    The 'Deprecation' class represents deprecations of functions or classes and is designed
    to be used with the ``warnings`` library.
	
    Parameters:
    =================================================================================================================
    last_supported_version: str
        Version string, eg ``'0.3.0'``.
    will_be_removed_in    : str, optional
        Version string, eg ``'1.0.0'``.
		
    use_instead           : object or str, optional
        Function or class to be used instead or descriptive string.
		
    issue                 : str, optional
    issue_url             : callback, optional
        Converts issue to url, for example ``lambda s: 'https://github.com/user/repo/issues/%s/' % s.strip('gh-')``
		
    warning               : DeprecationWarning, optional
        Any subclass of DeprecationWarning
    """
    _deprecations = {}

	def __init__(
		self,
		last_supported_verion = None
	):
		pass # do later
