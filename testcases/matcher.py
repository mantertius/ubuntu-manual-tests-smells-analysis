from collections import abc

import numpy as np
import spacy
#from pprint import pprint as print
from rich import print
from spacy import displacy

from data import Test, get_tests, k_closest_words, nlp, smells_loader
from dependency_matchers import MatchersFactory

def is_conditional_test(test:abc.Container) -> bool: #OK
    """
    1) It uses coordinating conjunctions, such as "and" or "or".
    2) Or uses a conditional "if".
    """
    matcher = MatchersFactory.conditional_test_matcher()
    for step in test.steps:
            matches = []
            action_matches = matcher(step.action)
            if action_matches:
                return True
    return False

def is_eager_step(test: abc.Container) -> bool: #OK!
    """
    More than one imperative verb per step
    """
    eager_step = 0
    steps = test.steps
    for step in steps:
        actions = [action for action in step.action if action.tag_ in ['VB', 'VBP']]
        eager_step = eager_step + len(actions)
    return eager_step > 0

def is_unverified_step(test: abc.Container) -> bool: #OK!
    """
    Missing verification step
    """
    steps = test.steps
    return len([step for step in steps if len(step.reactions) == 0]) > 0

def is_misplaced_precondition(test: abc.Container) -> bool: #naelson vai dar uma olhada
    matcher = MatchersFactory.misplaced_precondition_matcher()
    for step in test.steps:
        doc = nlp(step.action)
        for sentence in doc.sents:
            if matcher(sentence):
                print(sentence)
                return True
    return False

def is_bad_verification_format(test: abc.Container) -> bool:  #BAD VERIFICATION FORMAT
# There are more accurate methods which works even without the question mark egg: https://github.com/kartikn27/nlp-question-detection
    steps = test.steps
    bad_verification_format_steps = [step for step in test if '?' in steps]
    return len(bad_verification_format_steps) > 0

def is_misplaced_step(test: abc.Container) -> bool:
    """
    Steps usually come on the imperative format. Imperative sentences usually start with a verb in second person.
    https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    This function checks if one of the steps of a test is an imperative sentence.
    """
    def has_imperative_sentence(doc: spacy.tokens.Doc) -> bool:
        for sentence in doc.sents:
            if sentence[0].tag_ in ['VB', 'VBP']:
                return True
        return False

    steps = test.steps
    marked_steps = [
        step for step in steps for reaction in step.reactions if has_imperative_sentence(reaction)]
    return len(marked_steps) > 0

def is_undefined_wait(test: abc.Container) -> bool:
    matcher = MatchersFactory.undefined_wait_matcher()
    for step in test.steps:
            matches = []
            action_matches = matcher(step.action)
            if action_matches:
                return True
    return False

def is_misplaced_result(test: abc.Container) -> bool:
    """
    Checks for active pronouns on the test.reaction field.

    A verification verb (check, verify, observe, recheck) in the step description
    Declarative sentence after any imperative one in the steps
    something (must verb) - verbos modais de obrigatoriedade devem entrar na classificação de verbos de verificação
    """
    matcher = MatchersFactory.misplaced_result_matcher()
    for step in test.steps:
        matches = []
        action_matches = matcher(step.action)
        if action_matches:
            print(step.action)
            return True
    return False

def is_ambiguous_test(test: abc.Container) -> bool:
    """
    Imperative + indefinite pronoun/article
    list of options separated by slash '/ ' or between parenthesis and separated by slash, comma or pipe
    Use of 'etc.', 'different', 'multiple'
    Use of adverb of manner
    """
    pass


if __name__ == '__main__':
    # _in = input("Type the Manual Test Smell Acronym or the Posix Path:")
    # tests = get_tests(_in)

    tests = get_tests('PCAS')
    print(tests)
    counter = 0
    for Test in tests:
        cnt2 = 0
        for test in Test:
            result = is_misplaced_precondition(test)
            print(f'[{counter}] {test.file}[{cnt2}]: {result}')
            counter += 1
            cnt2 += 1
            #displacy.serve()
        # if not result:
        #     actions = [t.action for t in test]
        #     _actions = list(enumerate(actions))
        #     pprint(_actions)
        #     node = input('Which node to serve? ')
        #     displacy.serve(nlp(actions[int(node)]))
        # print(result)
        # print()
