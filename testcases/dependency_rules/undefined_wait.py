from data import expand_words

wait_words = expand_words(('wait', 'halt', 'rest', 'holdup'), k=3)

patterns = [
            [
                {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'LOWER': {'IN': wait_words}}},
            ],
            [
                {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'LOWER': {'IN': wait_words}}},
                {'RIGHT_ID': 'verb', 'LEFT_ID':'anchor', 'REL_OP': '<','RIGHT_ATTRS': {'LOWER': 'timeout'}},
            ]
        ]
#exemplo: Wait for the window to pop or until timeout.