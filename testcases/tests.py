from data import nlp
from spacy.matcher import DependencyMatcher
from spacy import displacy
wait_words = ('wait', 'halt', 'rest', 'holdup')

if __name__ == '__main__':
    text = 'I would like to buy a coke'
    doc = nlp(text)
    # displacy.serve(doc)
    matcher = DependencyMatcher(nlp.vocab)
    rule = \
            [
                {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'LOWER': {'IN': wait_words}}},
                {'RIGHT_ID': 'units','RIGHT_ATTRS': {}, 'LEFT_ID':'anchor', 'REL_OP': '>>'},
                {'RIGHT_ID': 'time', 'LEFT_ID':'units', 'REL_OP': '>','RIGHT_ATTRS': {'LIKE_NUM': True}},
            ]
    matcher.add('whatever', [rule])
    print(matcher(doc))