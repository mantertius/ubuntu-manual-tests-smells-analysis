#https://stackoverflow.com/questions/29473169/approach-for-identifying-whether-a-sentence-includes-an-imperative-within-it

#from data import expand_words

#ensure_like = expand_words(('ensure', 'check'), k=15)
# comps = ['aux', 'auxpass', 'cop']

# patterns = [
#             [
#                 {
#                     'RIGHT_ID': 'anchor',
#                     'RIGHT_ATTRS': {'POS': {'IN': ['VERB', 'VB'], 'IS_SENT_START' : True}}
#                 },
#                 {
#                     'RIGHT_ID': 'ccomp',
#                     'LEFT_ID': 'anchor',
#                     'RIGHT_ATTRS': {'DEP':{'IN': comps}},
#                     'REL_OP' : '<'
#                 },
#             ],
#         ]

patterns = [
            [
                {
                    'RIGHT_ID': 'noun',
                    'RIGHT_ATTRS': {'POS': {'IN': ['PROPN', 'NOUN']}}
                },

                {
                    'LEFT_ID': 'noun',
                    'RIGHT_ID': 'aux',
                    'RIGHT_ATTRS': {'POS': 'AUX', 'DEP': {'IN': ['aux', 'auxpass', 'cop']}},
                    'REL_OP': '.*'
                },
                {
                    'LEFT_ID': 'aux',
                    'RIGHT_ID': 'verb',
                    'RIGHT_ATTRS': {'POS': 'VERB'},
                    'REL_OP': '>'
                },
            ],
        ]

# patterns = [
#             [
#                 {'POS': 'AUX'}, {'POS': 'VERB'}
#             ],
#             [
#                 {'POS': 'AUX'}, {'POS': 'ADJ'}
#             ],
# [
#                 {'POS': 'AUX'}, {'POS': 'ADV'}
#             ]
#         ]

# patterns = [
#             [
#                 {'TAG': {'IN': ['NNP', 'NNS']}}, {'POS': 'AUX'}
#             ]
#         ]

#"RIGHT_ATTRS": {"DEP": "nsubj"}
#4 - Misplaced Pre-Condition
