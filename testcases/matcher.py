from collections import abc

try:
    from rich import print
except ModuleNotFoundError:
    pass

from data import get_tests, matcher_wait, matcher_if, matcher_optional


def is_unverified_step(test: abc.Container) -> bool:
    # breakpoint()
    steps = test.steps
    return len([step for step in steps if len(step.reactions) == 0]) > 0



def is_exception_handling(test: abc.Container) -> bool:
# There are more accurate methods which works even without the question mark egg: https://github.com/kartikn27/nlp-question-detection
    exceptional_steps = [step for step in test if '?' in step.action]
    return len(exceptional_steps) > 0


def is_eager_test(test: abc.Container) -> bool:
    eager_steps = [step for step in test if len(step.reactions) > 1]
    return len(eager_steps) > 0


def is_expected_results_as_step(test: abc.Container) -> bool:
    """
    Steps usually come on the imperative format. Imperative sentences usually start with a verb in second person.
    https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    This function checks if one of the steps of a test is an imperative sentence.
    """
    marked_steps = [
        step for step in test for reaction in step.reactions if reaction[0].tag_ in ['VB', 'VBP']]
    # breakpoint()
    return len(marked_steps) > 0


def is_undefined_wait(test: abc.Container) -> bool:
    # I don't know if this works!
    """
    Using a powerful regex matcher, we are able to locate expressions that have the "wait" but do not specify the wait time.
    https://spacy.io/api/matcher
    """
    smelly_step = [step for step in test if matcher_wait(step.action) > 0]
    smelly_result = [step for step in test if matcher_wait(step.reaction) > 0]
    return smelly_result+smelly_step > 0

def is_misplaced_result(test: abc.Container) -> bool:
    """
    Checks for active pronouns on the test.reaction field.
    """
    pass

def is_conditional_test(test: abc.Container) -> bool:
    # I don't know if this works!
    """
    Uses the spacy matcher to look for "if"s.
    """
    smelly_step = [step for step in test if matcher_if(step.action) > 0]
    smelly_result = [step for step in test if matcher_if(step.reaction) > 0]
    return smelly_result + smelly_step > 0

def is_optional_test(test: abc.Container) -> bool:
    """
    Uses the spacy matcher to look for "if"s.
    """
    smelly_header = [header for header in test if matcher_optional(header) > 0 ]
    smelly_step = [step for step in test if matcher_optional(step.action) > 0]
    smelly_result = [step for step in test if matcher_optional(step.reaction) > 0]
    return smelly_header + smelly_result + smelly_step > 0

def is_misplaced_pre_condition(test:abc.Container) -> bool:
    #As this one is kinda hard to detect using nlp, we should just send a warning, not an definitive "this is wrong"
    """
    Searches for "make sure", "ensure" and synomyms using spacy's matcher.
    """
    pass


if __name__ == '__main__':
    #_in = input("Type the Manual Test Smell Acronym or the Posix Path:")
    # get_tests está retornando uma tupla-> tests = test_list,path_list
    tests = get_tests("US")
    cnt = 0
    for Test in tests:
        cnt2 = 0
        for test in Test:
            print(f'[{cnt}] {test.file}: {is_unverified_step(test)}')
            cnt += 1
