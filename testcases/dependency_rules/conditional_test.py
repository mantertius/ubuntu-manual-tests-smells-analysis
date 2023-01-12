from data import expand_words

#conditional_words = expand_words(('if', 'whether', 'depending', 'when', 'case', 'otherwise'), k=3)
#breakpoint()
conditional_words = ['if','or']
patterns = [
            [
                {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'LOWER': {'IN': conditional_words}, 'DEP':'ROOT'}},
            ],
            [
                {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'LOWER': {'IN': conditional_words}}},
                {'RIGHT_ID': 'verb', 'LEFT_ID':'anchor', 'REL_OP': '<','RIGHT_ATTRS': {'POS': 'VERB'}},
            ]
        ]