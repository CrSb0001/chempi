from .util.pyutil import AttrContainer

def get_constant_symbol(Symbol = None):
	if Symbol is None:
		from sympy import Symbol
	
	consts = [
		('Faraday_constant'   , 'F'        ),
		('Avogadro_constant'  , 'N_A'      ),
		('vacuum_permittivity', 'epsilon_0'),
		('Boltzmann_constant' , 'k_B'      ),
		('pi'                 , 'pi'       ),
		('Molar_gas_constant' , 'R'        )
	]
	
	return AttrContainer(**{k: Symbol(v) for k, v in consts})
