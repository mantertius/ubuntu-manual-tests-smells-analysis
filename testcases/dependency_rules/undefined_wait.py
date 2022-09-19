from data import expand_words

wait_words = expand_words(("wait", "halt", "rest", "holdup", "stay on hold"), k=5)

patterns = [
            [
                {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'LOWER': {'IN': wait_words}}},
            ],
        ]
        # , 'DEP':'ROOT'
            # [
            #     {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'LOWER': {'IN': wait_words}}},
            #     {'RIGHT_ID': 'verb', 'LEFT_ID':'anchor', 'REL_OP': '<','RIGHT_ATTRS': {'POS': 'VERB'}},
            # ]