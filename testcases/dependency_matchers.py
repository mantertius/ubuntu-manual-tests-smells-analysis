from spacy.matcher import DependencyMatcher
import spacy
from data import nlp
from dependency_rules import unspecified_parameter, conditional_test, pre_condition_as_step_test

class MatchersFactory:
    def unspecified_parameter_matcher():
        return MatchersFactory._build_matcher(unspecified_parameter.patterns)

    def conditional_test_matcher():
        return MatchersFactory._build_matcher(conditional_test.patterns)

    def pre_condition_as_step():
        return MatchersFactory._build_matcher(pre_condition_as_step_test.patterns)

    def _build_matcher(patterns):
        matcher = DependencyMatcher(nlp.vocab)
        patterns = enumerate(patterns)
        for idx, pattern in patterns:
            matcher.add('rule'+str(idx), [pattern])
        return matcher

if __name__ == '__main__':
    a = 'Do any amount of coding on the database'
    m = unspecified_parameter_matcher()
    doc = nlp(a)
    r = m(doc)
    print(r)

