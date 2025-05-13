class _RxnTable(object):
    _rsys_method = None
    
    def __init__(
        self,
        idx_rxn_pairs,
        substances,
        colors = None,
        missing = None,
        missing_color = 'eee8aa'
    ):
        self.idx_rxn_pairs = idx_rxn_pairs
        self.substances    = substances
        self.colors        = colors  or {}
        self.missing       = missing or []
        self.missing_color = missing_color
    
    @classmethod
    def from_ReactionSystem(cls, rsys, color_cats = True):
        idx_rxn_pairs, unconsidered_ri = getattr(rsys, cls._rsys_method)()
        colors = rsys._category_colors() if color_cats else {}
        missing = [not rsys.substance_particip(sk) for sk in rsys.substances]
        return (cls(idx_rxn_pairs, rsys.substances, colors = colors, missing = missing), unconsidered_ri)
    
    def _repr_html(self):
        '''
        from .web import css
        
        return css(self, substances = self.substances, colors = self.colors)
        '''
        pass
    
    def _cell_label_html(self, printer, orig_idx, rxn):
        '''Reaction formatting callback.'''
        pretty = rxn.unicode(self.substances, with_param = True, with_name = False)
        return '<a title="%d: %s">%s<a>' % (orig_idx, pretty, printer._print(rxn.name or rxn.param))
