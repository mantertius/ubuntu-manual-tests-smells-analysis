import abc
from data import  expand_unispecific_words

UNSPECIFIC_WORDS = expand_unispecific_words()

pattern = [
            {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'POS': 'NOUN'}},
            {'RIGHT_ID': 'determinant','LEFT_ID':'anchor','REL_OP':'>', 'RIGHT_ATTRS': {'LOWER': {'IN': UNSPECIFIC_WORDS}}}
        ]