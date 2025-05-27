from collections import OrderedDict
from .pyutil     import defaultnamedtuple

DIMENSION_CODES = OrderedDict(
	zip(
		'length mass time current temperature amount'.split(), # will add luminous_intensity (cd) in the future
		'L M T I Θ N'.split()
	)
)

class DimensionalitySI(
	defaultnamedtuple(
		'DimensionalitySIBase',
		DIMENSION_CODES.keys(),
		(0,) * len(DIMENSION_CODES)
	)
):
	# __mul__, __truediv__, __pow__ on a logarithmic scale.
	
	def __mul__(self, other):
		return self.__class__(
			*(x + y for x, y in zip(self, other))
		)
	
	def __truediv__(self, other):
		return self.__class__(
			*(x - y for x, y in zip(self, other))
		)
	
	def __pow__(self, exp):
		return self.__class__(
			*(x * exp for x in self)
		)

BASE_REGISTRY = {
	name: DimensionalitySI(**{name: 1}) for name in DIMENSION_CODES
}
