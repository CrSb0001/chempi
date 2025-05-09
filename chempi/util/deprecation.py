import warnings

class Deprecation(object):
    """Decorator factory for deprecating functions/classes.
	
    The 'Deprecation' class represents deprecations of functions or classes and is designed
    to be used with the ``warnings`` library.
	
    Parameters:
    =================================================================================================================
    last_supported_version: str
        Version string, eg `'0.3.0'`.
    will_be_removed_in    : str, optional
        Version string, eg `'1.0.0'`.
	
    use_instead           : object or str, optional
        Function or class to be used instead or descriptive string.
	
    issue                 : str, optional
    issue_url             : callback, optional
        Converts issue to url, for example `lambda s: 'https://github.com/user/repo/issues/%s/' % s.strip('gh-')`
	
    warning               : DeprecationWarning, optional
        Any subclass of DeprecationWarning
    """
    _deprecations = {}
	
	def __init__(self, last_supported_verion, will_be_missing_in = None, use_instead = None, issue = None, issue_url = None, warning = DeprecationWarning):
	    if not isinstance(last_supported_version, (str, tuple, list)) and callable(last_supported_version):
		    raise ValueError("Parameter `last_supported_version` is not one of str, tuple, list")
		
		self.last_supported_version = last_supported_version
		self.will_be_missing_in = will_be_missing_in
		self.use_instead = use_instead
		self.issue = issue
		self.issue_url = issue_url
		self.warning = warning
		self.warning_msg = self._warning_msg_template()
	
    @classmethod
    def inspect(cls, obj):
        return cls._deprecations[obj]
		
    def _warning_msg_template():
        msg  = '%(func_name)s has been deprecated'
		msg += ' since (not including) %s' % self.last_supported_version
		if self.will_be_missing_in is not None:
			msg += ', it will be missing in %s' % self.will_be_missing_in
			
		if self.issue is not None:
			if self.issue_url is not None:
				msg += self.issue_url(self.issue)
			
			else:
				msg += ' (see issue %s)' % self.issue
		
		if self.use_instead is not None:
			try:
				msg += '. Use %s instead' % self.use_instead.__name__
			
			except AttributeError:
				msg += '. Use %s instead' % self.use_instead
		
		return msg + '.'
	
	def __call__(self, wrapped):
		"""Main attribute of the Deprecated class that wraps function"""
		msg = self.warning_message % {'func_name': wrapped.__name__}
		wrapped_doc = wrapped.__doc__ or ''
		if hasattr(wrapped, '__mro__'): # wrapped is a class method
			class _Wrapper(wrapped):
				__doc__ = msg + '\n\n' + wrapped_doc
				
				def __init__(_self, *args, **kwargs):
					warnings.warn(msg, self.warning, stacklevel = 2)
					wrapped.__init__(_self, *args, **kwargs)
		
		else: # wrapped is a function
			def _Wrapper(wrapped):
				warnings.warn(msg, self.warning, stacklevel = 2)
				return wrapped(*args, **kwargs)
			
			_Wrapper.__doc__ = msg + '\n\n' + wrapped_doc
		
		self._deprecations[_Wrapper] = self
		_Wrapper.__name__   = wrapped.__name__
		_Wrapper.__module__ = wrapped.__module__
		return _Wrapper
