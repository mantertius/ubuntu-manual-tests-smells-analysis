from collections import abc
try:
    from rich import print
except ModuleNotFoundError:
    pass

from data import get_tests, smells_loader

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

if __name__ == '__main__':
    _in = input("Type the Manual Test Smell Acronym or the Posix Path:")
    tests = get_tests(_in)
    for test in tests:
        print(f'{is_expected_results_as_step(test)}')