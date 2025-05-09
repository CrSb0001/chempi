# The data in '_relative_atomic_masses' is licensed under the CC-SA license
# https://en.wikipedia.org/wiki/Standard_atomic_weight#List_of_atomic_weights
_elements = [
    # [Symbol: str, Name: str, Relative Atomic Mass: float | str, Uncertainty: float]
    ['H', 'Hydrogen', 1.008,  1e-4],
    ['He', 'Helium',  4.002602, 2e-06],
    ['Li', 'Lithium', 6.94, 0.06],
    ['Be', 'Beryllium', 9.01221831, 5e-07],
    ['B', 'Boron', 10.81, 0.0],
    ['C', 'Carbon', 12.011, 0.0],
    ['N', 'Nitrogen', 14.007, 0.0],
    ['O', 'Oxygen', 15.999, 0.0],
    ['F', 'Fluorine', 18.998403162, 5e-9],
    ['Ne', 'Neon', 20.1797, 6e-4],
    ['Na', 'Sodium', 22.98976928, 2e-8],
    ['Mg', 'Magnesium', 24.305, 0.002] # Finish later
]

_SYMBOLS     = tuple(n[0] for n in _elements)
_NAMES       = tuple(n[1] for n in _elements)
_LOWER_NAMES = tuple(n[1].lower() for n in _elements)

_PERIOD_LENGTHS = (2, 8, 8, 18, 18, 32, 32)
_ACCUM_PERIOD_LENGTHS = (2, 10, 18, 36, 54, 86, 118)

GROUPS     = {g: tuple(x - 18 + g for x in _ACCUM_PERIOD_LENGTHS[1:]) for g in range(13, 18)}
GROUPS[1]  = (1,) + tuple(x + 1 for x in _ACCUM_PERIOD_LENGTHS[:-1]) # Alkali metals
GROUPS[2]  = tuple(x + 2 for x in _ACCUM_PERIOD_LENGTHS[:-1]) # Alkaline earth metals
GROUPS[18] = _ACCUM_PERIOD_LENGTHS # Noble gasses

def atomic_number(name):
    '''
    Provides the atomic number for a given element
    '''
    try:
        return _SYMBOLS.index(name.capitalize()) + 1
    
    except:
        return _LOWER_NAMES.index(name.lower()) + 1

def _get_relative_atomic_masses():
    for mass in tuple(element[2] for element in _elements):
        yield float(mass[1:-1]) if str(mass)[0] == '[' else float(mass)

RELATIVE_ATOMIC_MASSES = tuple(_get_relative_atomic_masses())

def mass_from_composition(composition):
    '''
    Calculates molecular mass given a dict object of atomic weights.
    
    Notes
    ==================
    Atomic number `0` represents charge, aka 'net electron deficiency'
    
    
    Examples:
    ==================
    >>> mass_from_composition({0: -1, 1: 1, 8: 1})
    17.01
    '''
    mass = 0.0
    for k, v in composition.items():
        if k == 0:
            mass -= v * 5.489e-4
        
        else:
            mass += v * RELATIVE_ATOMIC_MASSES[k - 1]
    
    return mass
