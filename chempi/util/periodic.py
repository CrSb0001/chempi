# The data in '_relative_atomic_masses' is licensed under the CC-SA license
# https://en.wikipedia.org/wiki/Standard_atomic_weight#List_of_atomic_weights
_elements = [
    # [Symbol: str, Name: str, Relative Atomic Mass: float | str, Uncertainty: float]
    ['H', 'Hydrogen', 1.008,  1e-4],
    ['He', 'Helium',  4.002602, 2e-06],
    ['Li', 'Lithium', 6.94, 0.06],
    ['Be', 'Beryllium', 9.01221831, 5e-07],
    ['B', 'Boron', 10.81, 0.02],
    ['C', 'Carbon', 12.011, 0.002],
    ['N', 'Nitrogen', 14.007, 0.001],
    ['O', 'Oxygen', 15.999, 0.001],
    ['F', 'Fluorine', 18.998403162, 5e-9],
    ['Ne', 'Neon', 20.1797, 6e-4],
    ['Na', 'Sodium', 22.98976928, 2e-8],
    ['Mg', 'Magnesium', 24.305, 0.002],
    ['Al', 'Aluminium', 26.9815384, 3e-7],
    ['Si', 'Silicon', 28.085, 0.001],
    ['P', 'Phosphorus', 30.973761998, 5e-9],
    ['S', 'Sulfur', 32.06, 0.02],
    ['Cl', 'Chlorine', 35.45, 0.01],
    ['Ar', 'Argon', 39.95, 0.16],
    ['K', 'Potassium', 39.0983, 1e-4],
    ['Ca', 'Calcium', 40.078, 0.004],
    ['Sc', 'Scandium', 44.955907, 4e-6],
    ['Ti', 'Titanium', 47.867, 0.001],
    ['V', 'Vanadium', 50.9415, 1e-4],
    ['Cr', 'Chromium', 51.9961, 6e-4],
    ['Mn', 'Manganese', 54.938, 0.001],
    ['Fe', 'Iron', 55.845, 0.002],
    ['Co', 'Cobalt', 58.933194, 3e-6],
    ['Ni', 'Nickel', 58.693, 0.001],
    ['Cu', 'Copper', 63.546, 0.003],
    ['Zn', 'Zinc', 65.38, 0.02],
    ['Ga', 'Gallium', 69.723, 0.001],
    ['Ge', 'Germanium', 72.63, 0.008],
    ['As', 'Arsenic', 74.921595, 6e-6],
    ['Se', 'Selenium', 78.971, 0.008],
    ['Br', 'Bromine', 79.904, 0.003],
    ['Kr', 'Krypton', 83.798, 0.002],
    ['Rb', 'Rubidium', 85.4678, 3e-4],
    ['Sr', 'Strontium', 87.62, 0.01],
    ['Y', 'Yttrium', 88.905838, 2e-6],
    ['Zr', 'Zirconium', 91.222, 0.003],
    ['Nb', 'Niobium', 92.90637, 1e-5],
    ['Mo', 'Molybdenum', 95.95, 0.01],
    ['Tc', 'Technetium', '[98]', 0.0],
    ['Ru', 'Ruthenium', 101.07, 0.02],
    ['Rh', 'Rhodium', 102.90549, 2e-5],
    ['Pd', 'Palladium', 106.42, 0.01],
    ['Ag', 'Silver', 107.8682, 2e-4],
    ['Cd', 'Cadmium', 112.414, 0.004],
    ['In', 'Indium', 114.818, 0.001],
    ['Sn', 'Tin', 118.71, 0.01],
    ['Sb', 'Antimony', 121.76, 0.01],
    ['Te', 'Tellurium', 127.60, 0.03],
    ['I', 'Iodine', 126.90447, 3e-5],
    ['Xe', 'Xenon', 131.293, 0.006],
    ['Cs', 'Caesium', 132.90545196, 6e-8],
    ['Ba', 'Barium', 137.327, 0.007],
    ['La', 'Lanthanum', 138.90547, 7e-5],
    ['Ce', 'Cerium', 140.12, 0.01],
    ['Pr', 'Praseodymium', 140.97066, 1e-5],
    ['Nd', 'Neodymium', 144.24, 0.01],
    ['Pm', 'Promethium', '[145]', 0.0],
    ['Sm', 'Samarium', 150.36, 0.02],
    ['Eu', 'Europium', 151.96, 0.01],
    ['Gd', 'Gadolinium', 157.249, 0.002],
    ['Tb', 'Terbium', 158.925354, 7e-6],
    ['Dy', 'Dysprosium', 162.50, 0.01],
    ['Ho', 'Holmium', 164.930329, 5e-6],
    ['Er', 'Erbium', 167.259, 0.003],
    ['Tm', 'Thulium', 168.934219, 5e-6],
    ['Yb', 'Ytterbium', 173.05, 0.02],
    ['Lu', 'Lutetium', 174.97, 0.01],
    ['Hf', 'Hafnium', 178.49, 0.01],
    ['Ta', 'Tantalum', 180.95, 0.01],
    ['W', 'Tungsten', 183.84, 0.01],
    ['Re', 'Rhenium', 186.21, 0.01],
    ['Os', 'Osmium', 190.23, 0.03],
    ['Ir', 'Iridium', 192.22 0.01],
    ['Pt', 'Platinum', 195.08, 0.02],
    ['Au', 'Gold', 196.97, 0.01],
    ['Hg', 'Mercury', 200.59, 0.01],
    ['Tl', 'Thallium', 204.38, 0.01],
    ['Pb', 'Lead', 207.20, 1.1],
    ['Bi', 'Bismuth', 208.98, 0.01],
    ['Po', 'Polonium', '[209]', 0.0],
    ['At', 'Astatine', '[210]', 0.0],
    ['Rn', 'Radon', '[222]', 0.0],
    ['Fr', 'Francium', '[223]', 0.0],
    ['Ra', 'Radium', '[226]', 0.0],
    ['Ac', 'Actinium', '[227]', 0.0],
    ['Th', 'Thorium', 232.04, 0.01],
    ['Pa', 'Protactinium', 231.04, 0.01],
    ['U', 'Uranium', 238.03, 0.01],
    ['Np', 'Neptunium', '[237]', 0.0],
    ['Pu', 'Plutonium', '[244]', 0.0],
    ['Am', 'Americium', '[243]', 0.0],
    ['Cm', 'Curium', '[247]', 0.0],
    ['Bk', 'Berkelium', '[247]', 0.0],
    ['Cf', 'Californium', '[251]', 0.0],
    ['Es', 'Einsteinium', '[252]', 0.0],
    ['Fm', 'Fermium', '[257]', 0.0],
    ['Md', 'Mendelevium', '[258]', 0.0],
    ['No', 'Nobelium', '[259]', 0.0],
    ['Lr', 'Lawrencium', '[266]', 0.0],
    ['Rf', 'Rutherfordium', '[267]', 0.0],
    ['Db', 'Dubnium', '[268]', 0.0],
    ['Sg', 'Seaborgium', '[269]', 0.0],
    ['Bh', 'Bohrium', '[270]', 0.0],
    ['Hs', 'Hassium', '[271]', 0.0],
    ['Mt', 'Meitnerium', '[278]', 0.0],
    ['Ds', 'Darmstadtium', '[281]', 0.0],
    ['Rg', 'Roentgenium', '[282]', 0.0],
    ['Cn', 'Copernicium', '[285]', 0.0],
    ['Nh', 'Nihonium', '[286]', 0.0],
    ['Fl', 'Flerovium', '[289]', 0.0],
    ['Mc', 'Moscovium', '[290]', 0.0],
    ['Lv', 'Livermorium', '[293]', 0.0],
    ['Ts', 'Tennessine', '[294]', 0.0],
    ['Og', 'Oganesson', '[294]', 0.0]
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
