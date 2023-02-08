import sys
from rich import print
from keywords import Keywords
from data import get_tests
import matchers
import pandas as pd

try:
    Keywords(sys.argv[1]) #Instantiates the singleton Keyword objects with the selected language
except IndexError:
    Keywords('english')

if __name__ == '__main__':

    print('Retrieving tests...')
    tests = get_tests('')
    print(f'Total tests: {len(tests)}')

    print('Analyzing...')
    for (file_index, test_file) in enumerate(tests):
        for (test_index, test) in enumerate(test_file):
            matchers.find_ambiguous_test(test_index, test)
            matchers.find_conditional_test_logic(test_index, test)
            matchers.find_eager_step(test_index, test)
            matchers.find_unverified_step(test_index, test)
            matchers.find_misplaced_step(test_index, test)
            matchers.find_misplaced_result(test_index, test)
            matchers.find_misplaced_precondition(test_index, test)

    print('Analysis complete!')