from collections import abc

import numpy as np
import spacy
#from pprint import pprint as print
from rich import print
from spacy import displacy

from data import (Test, get_tests, k_closest_words, matcher_if, matcher_optional,
                  matcher_wait, nlp, smells_loader)
from dependency_matchers import MatchersFactory


def is_unverified_step(test: abc.Container) -> bool:
    steps = test.steps
    return len([step for step in steps if len(step.reactions) == 0]) > 0

def is_precondition_as_step(tests: abc.Container) -> bool:
    matcher = MatchersFactory.pre_condition_as_step_matcher()
    for test in tests:
        for step in test.steps:
            doc = nlp(step.action)
            for sentence in doc.sents:
                if matcher(sentence):
                    return True
    return False

def is_exception_handling(test: abc.Container) -> bool:
# There are more accurate methods which works even without the question mark egg: https://github.com/kartikn27/nlp-question-detection
    exceptional_steps = [step for step in test if '?' in step.action]
    return len(exceptional_steps) > 0

def is_eager_test(test: abc.Container) -> bool:
    eager_test = [step for step in test if len(step.reactions) > 1]
    return len(eager_test) > 0

def is_eager_step(test: abc.Container) -> bool:
    eager_step = [step for step in test for action in step.actions if action[0].tag_ in ['VB', 'VBP']]
    return len(eager_step) > 0

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
    # breakpoint()
    return len(marked_steps) > 0

def is_unspecified_parameter(test:abc.Container) -> bool:
    matcher = MatchersFactory.unspecified_parameter_matcher()
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
    matcher = MatchersFactory.conditional_test_matcher()
    for step in test.steps:
            #breakpoint()
            matches = []
            action_matches = matcher(step.action)
            if action_matches:
                return True
    return False

def is_undefined_wait(test: abc.Container) -> bool:
    matcher = MatchersFactory.undefined_wait_matcher()
    for step in test.steps:
            #breakpoint()
            matches = []
            action_matches = matcher(step.action)
            if action_matches:
                return True
    return False

def is_optional_test(test: abc.Container) -> bool:
    matcher = MatchersFactory.optional_test_matcher()
    for step in test.steps:
            matches = []
            action_matches = matcher(step.action)
            header_matches = matcher(test.header)
            any_match = action_matches+header_matches
            if action_matches:
                return True
    return False

def is_test_clone(test: Test, other_tests:abc.Container = None) -> bool:
    other_tests = get_tests('')
    (header, steps) = (test.header, test.steps)
    for file_test in other_tests:
        for other_test in file_test:
            (other_header, other_steps) = (other_test.header, other_test.steps)
    return None









# def is_undefined_wait(test: abc.Container) -> bool:
#     # I don't know if this works!
#     """
#     Using a powerful regex matcher, we are able to locate expressions that have the "wait" but do not specify the wait time.
#     https://spacy.io/api/matcher
#     """
#     smelly_step = [step for step in test if matcher_wait(step.action) > 0]
#     smelly_result = [step for step in test if matcher_wait(step.reaction) > 0]
#     return smelly_result+smelly_step > 0

def is_misplaced_result(test: abc.Container) -> bool:
    """
    Checks for active pronouns on the test.reaction field.
    """
    pass



#if __name__ == '__main__':
    #_in = input("Type the Manual Test Smell Acronym or the Posix Path:")
    # get_tests está retornando uma tupla-> tests = test_list,path_list
#    tests = get_tests("US")
#    cnt = 0
#    for Test in tests:
#        cnt2 = 0
#       for test in Test:
#            print(f'[{cnt}] {test.file}: {is_unverified_step(test)}')
#            cnt += 1

if __name__ == '__main__':
    # _in = input("Type the Manual Test Smell Acronym or the Posix Path:")
    # tests = get_tests(_in)
    tests = get_tests('ERAS')
    print(tests)
    cnt = 0
    for Test in tests:
        cnt2 = 0
        for test in Test:
            result = is_test_clone(test)
            print(f'[{cnt}] {test.file}[{cnt2}]: {result}')
            cnt += 1
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
