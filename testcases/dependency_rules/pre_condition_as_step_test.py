#https://stackoverflow.com/questions/29473169/approach-for-identifying-whether-a-sentence-includes-an-imperative-within-it

from data import expand_words

ensure_like = expand_words(('ensure', 'check'), k=15)

patterns = [
            [
                {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'POS': {'IN': ['VERB', 'VB'], 'LOWER': {'IN': ensure_like}}, 'IS_SENT_START':True}}
            ]
        ]