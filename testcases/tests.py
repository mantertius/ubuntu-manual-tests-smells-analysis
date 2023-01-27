from data import nlp
from spacy.matcher import DependencyMatcher


if __name__ == '__main__':
    text = 'Wait for the window to pop or until timeout'
    doc = nlp(text)
    matcher = DependencyMatcher(nlp.vocab)
    rule = [
                {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'LOWER': {'IN': wait_words}}},
                {'RIGHT_ID': 'time', 'LEFT_ID':'anchor', 'REL_OP': '<','RIGHT_ATTRS': {'LIKE_NUM': True}, 'OP': '!'},
            ]
    matcher.add('whatever', [rule])
    print(matcher(doc))