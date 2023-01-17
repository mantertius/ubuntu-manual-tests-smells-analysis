from data import expand_words

actions = ('check', 'verify', 'observe', 'recheck')
actions = expand_words(actions, k=5)

patterns = [
            [
                {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'LOWER': {'IN': actions}, 'IS_SENT_START': True}}
            ]
        ]