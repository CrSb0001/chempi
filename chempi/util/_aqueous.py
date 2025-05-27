from itertools import chain
from .periodic import GROUPS, _NAMES, _SYMBOLS

_ANIONS = {
	'F-'      : 'fluoride',
	'Cl-'     : 'chloride',
	'Br-'     : 'bromide',
	'I-'      : 'iodide',
	'OH-'     : 'hydroxide',
	'CN-'     : 'cyanide',
	'SCN-'    : 'thiocyanate',
	'CO3-2'   : 'carbonate',
	'C2O4-2'  : 'oxalate',
	'HCO3-'   : 'hydrogencarbonate',
	'NO3-'    : 'nitrate',
	'NO2-'    : 'nitrite',
    'PO4-3'   : 'phospahte',
	'HPO4-2'  : 'hydrogenphospahte',
	'H2PO4-'  : 'dihydrogenphospahte',
	'P-3'     : 'phosphide',
	'SO4-2'   : 'sulphate',
	'HSO4-'   : 'hydrogensulphate',
	'SO3-2'   : 'sulphite',
	'HSO3-'   : 'hydrogensulphite',
	'S-2'     : 'sulfide',
	'ClO-'    : 'hypochlorite',
	'ClO2-'   : 'chlorite',
	'ClO3-'   : 'chlorate',
	'ClO4-'   : 'perchlorate',
	'CrO4-2'  : 'chromate(VI)',
	'Cr2O7-2' : 'dichromate(VI)',
	'MnO4-2'  : 'manganate(VI)',
	'MnO4-'   : 'permanganate(VII)',
	'FeO4-2'  : 'ferrate(VI)',
	'OsO4-2'  : 'osmate(VI)',
	'Bo3-3'   : 'borate',
	'BiO3-'   : 'bismuthate(V)'
}

_CATIONS = {
	'H3O+': 'hydronium'
}

_CATION_OXIDATION_STATES = { # more likely states
	'Al': (      3,   ),
	'Cr': (   2, 3    ),
	'Mn': (   2,      ),
	'Fe': (   2, 3    ),
	'Co': (   2, 3    ),
	'Ni': (   2, 3    ),
	'Cu': (1, 2, 3    ),
	'Zn': (   2,      ),
	'Ga': (      3,   ),
	'Ag': (1, 2       ),
	'Cd': (   2,      ),
	'In': (      3,   ),
	'Sn': (   2,    4,),
	'Sb': (      3,   ),
	'Au': (      3,   ),
	'Hg': (1, 2       ),
	'Tl': (1,    3    ),
	'Pb': (   2,    4 ),
	'Bi': (      3,   )
}

_ALKALI = [
	(
		_SYMBOLS[n] + '+',
		_NAMES[n].lower()
	) for n in GROUPS[1]
]
_ALKALINE_EARTH = [
	(
		_SYMBOLS[n] + '+2',
		_NAMES[n].lower()
	) for n in GROUPS[2]
]

_ALL_NAMES = dict(
	chain(
		_ALKALI,
		_ALKALINE_EARTH,
		_ANIONS.items()
	)
)

def name_(ion):
	return _ALL_NAMES[ion]
