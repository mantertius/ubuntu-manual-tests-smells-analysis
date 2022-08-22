from collections import abc

try:
    from rich import print
except ModuleNotFoundError:
    pass

import numpy as np

from data import get_tests, k_closest_words, nlp, smells_loader
from dependency_matchers import Matchers


def is_unverified_step(test:abc.Container) -> bool:
    return len([step for step in test if len(step.reactions) == 0]) > 0



# There are more accurate methods which works even without the question mark egg: https://github.com/kartikn27/nlp-question-detection
def  is_exception_handling(test:abc.Container) -> bool:
    exceptional_steps = [step for step in test if '?' in step.action]
    return len(exceptional_steps) > 0



def is_eager_test(test:abc.Container) -> bool:
    eager_steps = [step for step in test if len(step.reactions) > 1]
    return len(eager_steps) > 0



def is_expected_results_as_step(test:abc.Container) -> bool:
    """
    Steps usually come on the imperative format. Imperative sentences usually start with a verb in second person.
    https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    This function checks if one of the steps of a test is an imperative sentence.
    """
    marked_steps = [step for step in test for reaction in step.reactions  if reaction[0].tag_ in ['VB', 'VBP']]
    return len(marked_steps) > 0

def is_unspecified_parameter(test:abc.Container) -> bool:
    matcher = Matchers.unspecified_parameter_matcher()
    for step in test:
        matches = []
        action_matches = matcher(step.action)
        if action_matches:
            if action_matches:
                return True
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            if reaction_matches:
                return True
    return False

def is_conditional_test(test:abc.Container) -> bool:
    matcher = Matchers.conditional_test_matcher()
    for step in test:
        matches = []
        action_matches = matcher(step.action)
        if action_matches:
            if action_matches:
                return True
    return False

if __name__ == '__main__':
    from pprint import pprint
    from spacy import displacy
    # _in = input("Type the Manual Test Smell Acronym or the Posix Path:")
    # tests = get_tests(_in)
    tests = get_tests('CT')
    for test in tests:
        result = is_conditional_test(test)
        if not result:
            actions = [t.action for t in test]
            _actions = list(enumerate(actions))
            pprint(_actions)
            node = input('Which node to serve? ')
            displacy.serve(nlp(actions[int(node)]))
        # print(result)
        # print()
