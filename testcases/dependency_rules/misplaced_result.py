from keywords import Keywords

keywords = Keywords()
actions = keywords.keywords['actions']

patterns = [
            [
                {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'LOWER': {'IN': actions}, 'IS_SENT_START': True}}
            ],
        ]