#https://stackoverflow.com/questions/29473169/approach-for-identifying-whether-a-sentence-includes-an-imperative-within-it

from data import expand_words

ensure_like = expand_words(('ensure', 'check'), k=15)
comps = ['xcomp', 'ccomp']

patterns = [
            [
                {
                    'RIGHT_ID': 'anchor',
                    'RIGHT_ATTRS': {'POS': {'IN': ['VERB', 'VB'], 'IS_SENT_START' : True}}
                },
                {
                    'RIGHT_ID': 'ccomp',
                    'LEFT_ID': 'anchor',
                    'RIGHT_ATTRS': {'DEP':{'IN': comps}},
                    'REL_OP' : '<'
                },
            ],
        ]



# patterns = [
#             [
#                 {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'POS': {'IN': ['VERB', 'VB']}, 'IS_SENT_START':True}},
#             ]
#         ]

#"RIGHT_ATTRS": {"DEP": "nsubj"}
#4 - Misplaced Pre-Condition
