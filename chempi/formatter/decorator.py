from functools import wraps

def memoize_formatter(f, cache = {}):
	@wraps(f)
	def _g(*args, **kwargs):
		key = (
			f,
			tuple(args),
			frozenset(kwargs.items())
		)
		if key not in cache:
			cache[key] = f(*args, **kwargs)
		
		return cache[key].copy()
	
	return g

class with_doc:
	'''
 	Decorator that combines the docstrings of the provided
  	and decorated objects to produce one docstring
 	'''
	def __init__(
		self,
		method,
		use_header = True
	):
		self.method = method
		if use_header:
			self.header = '\n\n\tNotes\n\t-----\n'
		
		else:
			self.header = ''
	
	def __call__(
		self,
		new_method
	):
		new_doc = new_method.__doc__
		ori_doc = self.method.__doc__
		header  = self.header
		
		if ori_doc and new_doc:
			new_method.__doc__ = '\n\t{}\n\t{}\n\t{}'.format(ori_doc, header, new_doc)
		
		elif ori_doc:
			new_method.__doc__ = ori_doc
		
		return new_method
