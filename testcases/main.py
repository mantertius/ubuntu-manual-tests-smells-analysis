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
    # _in = input("Type the Manual Test Smell Acronym or the Posix Path:")
    # tests = get_tests(_in)

    print('Commencing analysis...')

    tests = get_tests('')
    # tests = get_tests('PCAS')
    print(f'Total tests: {len(tests)}')

    for (file_index, test_file) in enumerate(tests):
        for (test_index, test) in enumerate(test_file):
            # matchers.find_ambiguous_test(test)
            # matchers.find_conditional_test_logic(test)
            # matchers.find_eager_step(test)
            # matchers.find_unverified_step(test)
            # matchers.find_misplaced_step(test)
            matchers.find_misplaced_result(test)
            # matchers.find_misplaced_precondition(test)

            # result = matchers.is_misplaced_precondition(test)
            # print(f'[{test_index}] {test.file}[{file_index}]: {result}\n')

            # if not result:
            #     print(test)
            # displacy.serve()

    print('Analysis complete. Please open the results.csv file for detailed information.')