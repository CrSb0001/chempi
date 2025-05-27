from numpy import (
	atleast_1d,
	concatenate,
	empty,
	ndim,
	reshape,
	shape
)


def brodcast_stack(
	*args,
	**kwargs
):
	as_scalars = kwargs.pop('as_scalars', False)
	
	if kwargs != {}:
		raise ValueError(
			f'Received unexpected/unknown kwargs: {kwargs}'
		)
	
	args = [atleast_1d(arg) for arg in args]
	if as_scalars:
		args = [
			arg.reshape(arg.shape + (1,)) if arg.size > 1 else arg for arg in args
		]
	
	if all([arg.ndim == 1 for arg in args]):
		return concatenate(args)
	
	head_shape  = ()
	lead_length = 0
	
	for arg in args:
		lead_length += arg.shape[-1]
		if arg.ndim > 1:
			if head_shape == ():
				head_shape = arg.shape[:-1]
			
			elif arg.shape[:-1] != head_shape:
				raise ValueError(
					f'Shapes {arg.shape[:-1]} and {head_shape} are incompatible.'
				)
	
	out = empty(head_shape + (lead_length,))
	for idx, arg in enumerate(args):
		if arg.shape[-1] != 1:
			raise ValueError(
				f'Trailing dimension needs to be 1, found {arg} with trailing dim {arg.shape[-1]}.'
			)
		
		out[..., idx] = arg[..., 0]
	
	return out
