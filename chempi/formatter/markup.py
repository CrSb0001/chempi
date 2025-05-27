import copy
import operator
import re
import threading

class _Config:
	def __init__(self):
		self._lock        = threading.RLock()
		self._use_unicode = False
	
	@property
	def lock(self):
		return self._lock
	
	@property
	def use_unicode_(self):
		with self._lock:
			return copy.copy(self._use_unicode)
	
	@use_unicode_.setter
	def use_unicode(self, val):
		self._use_unicode = bool(val)

config = _Config()
superscripts = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']

def superscript(val):
	items = re.split(r'\*{2}([\d]+)(?!\.)', val)
	ret   = []
	
	while items:
		try:
			s = items.pop(0)
			e = items.pop(0)
			
			ret += [s + ''.join(superscripts[int(i)] for i in e)]
		
		except IndexError:
			ret += [s]
	
	return ''.join(ret)

def format_units(udict):
	pass

def format_units_html(
	udict,
	font  = '%s',
	mult  = r'&sdot',
	paren = False
):
	pass
