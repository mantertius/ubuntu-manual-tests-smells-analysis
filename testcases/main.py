import sys
from rich import print
from keywords import Keywords
from data import get_tests
import matchers


Keywords(sys.argv[1]) #Instantiates the singleton Keyword objects with the selected language

if __name__ == '__main__':
    # _in = input("Type the Manual Test Smell Acronym or the Posix Path:")
    # tests = get_tests(_in)

    tests = get_tests('AmbT')
    # tests = get_tests('PCAS')
    print(tests)
    counter = 0
    for (file_index, test_file) in enumerate(tests):
        for (test_index, test) in enumerate(test_file):
            result = matchers.is_misplaced_precondition(test)
            print(f'[{test_index}] {test.file}[{file_index}]: {result}\n')
            if not result:
                print(test)
            #displacy.serve()