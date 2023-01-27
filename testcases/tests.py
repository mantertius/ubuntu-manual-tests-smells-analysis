from data import nlp
from spacy.matcher import DependencyMatcher


if __name__ == '__main__':
    text = 'Wait for the window to pop or until timeout'
    doc = nlp(text)
    matcher = DependencyMatcher(nlp.vocab)
    rule = [
                {
                    'RIGHT_ID': 'anchor',
                    'RIGHT_ATTRS': {'POS': {'IN': ['VERB', 'VB'], 'IS_SENT_START' : True}}
                }
            ]
    matcher.add('whatever', [rule])
    print(matcher(doc))