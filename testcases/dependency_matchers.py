from spacy.matcher import DependencyMatcher
import spacy
from data import nlp

def unspecified_parameter_matcher():
    from dependency_rules.unspecified_parameter import pattern
    matcher = DependencyMatcher(nlp.vocab)
    matcher.add('unspecifiedparameter', [pattern])
    return matcher

if __name__ == '__main__':
    a = 'Do any amount of coding on the database'
    m = unspecified_parameter_matcher()
    doc = nlp(a)
    r = m(doc)
    print(r)

