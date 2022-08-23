import abc
from data import expand_words

conditional_words = expand_words(('if', 'whether', 'depending', 'when', 'case', 'otherwise'))

patterns = [
            [
                {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'LOWER': {'IN': conditional_words}, 'DEP':'ROOT'}},
            ],
            [
                {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'LOWER': {'IN': conditional_words}}},
                {'RIGHT_ID': 'verb', 'LEFT_ID':'anchor', 'REL_OP': '<','RIGHT_ATTRS': {'POS': 'VERB'}},
            ]
        ]