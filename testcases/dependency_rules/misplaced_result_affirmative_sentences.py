patterns = [
            [
                # anchor token: verb
                {
                    'RIGHT_ID': 'verb',
                    'RIGHT_ATTRS': {'POS': 'VERB'}
                },
                # verb -> subject
                {
                    "LEFT_ID": "verb",
                    "REL_OP": ">",
                    'RIGHT_ID': 'subject',
                    'RIGHT_ATTRS': {'POS': 'NOUN', 'DEP': {'IN': ['nsubj', 'nsubjpass']}}
                },
                # verb -> auxiliary
                {
                    'LEFT_ID': 'verb',
                    'REL_OP': '>',
                    'RIGHT_ID': 'auxiliary',
                    'RIGHT_ATTRS': {'POS': 'AUX', 'DEP': {'IN': ['aux', 'auxpass', 'cop']}}
                },
            ],
        ]
