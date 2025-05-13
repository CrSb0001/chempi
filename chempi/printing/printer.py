from itertools import chain

class Printer(object):
    '''
    Printer class method
    '''
    _str = str
    _default_settings = dict(
        with_param = True,
        with_name = True,
        fallback_print_fn = str,
        REACTION_PARAM_SEPARATOR = '; ',
        REACTION_COEFF_SPACE = ' ',
        REACTION_AROUND_ARROW = (' ', ' '),
        MAGNITUDE_FMT = lambda x: '%.3g' % x
    )
    _default_settings_factories = dict(
        substances = dict,
        colors = dict
    )
    _default_settings_attributes = dict(
        REACTION_COEFF_FMT = '_str',
        REACTION_FORMULA_FMT = '_str',
        unit_fmt = '_str'
    )
    print_method_attr = (None)
    
    def __init__(self, settings = None):
        self._settings = dict(self._default_settings, **(settings or {}))
        for k, v in self._default_settings_factories.items():
            if k not in self._settings:
                self._settings[k] = v()
        
        for k, v in self._default_settings_attributes.items():
            if k not in self._settings:
                self._settings[k] = getattr(self, v)
        
        for k in self._settings:
            if k not in chain(self._default_settings, self._default_settings_factories, self._default_settings_attributes):
                raise ValueError('Unknown setting: %s (missing in default settings)' % k)
    
    def _get(self, key, **kwargs):
        return kwargs.get(key, self._settings[key])
    
    def _print(self, obj, **kwargs):
        for cls in type(obj).__mro__:
            print_method = '_print_' + cls.__name__
            if hasattr(self, print_method):
                return getattr(self, print_method)(obj, **kwargs)
            
            for PrintCls in self.__class__.__mro__:
                _attr = getattr(PrintCls, 'printmethod_attr', None)
                if _attr and hasattr(obj, _attr):
                    return getattr(obj, _attr)(self, **kwargs)
        
        fn = self._get('fallback_print_fn', **kwargs)
        if fn:
            return fn(obj)
        
        raise ValueError('Don\'t know how to print object of type %s' % type(obj))
    
    def doprint(self, obj):
        return self._print(obj)
