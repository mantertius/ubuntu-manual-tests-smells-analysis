import sys
from rich import print
from keywords import Keywords
from data import get_tests
from ubuntu_matcher import get_tests as ubuntu_get_tests
import matchers


Keywords(sys.argv[1]) #Instantiates the singleton Keyword objects with the selected language

if __name__ == '__main__':
    # _in = input("Type the Manual Test Smell Acronym or the Posix Path:")
    # tests = get_tests(_in)

    # tests = get_tests('AmbT')
    tests = get_tests('AmbT')
    print(tests)
    counter = 0
    for Test in tests:
        cnt2 = 0
        for test in Test:
            result = matchers.is_misplaced_precondition(test)
            print(f'[{counter}] {test.file}[{cnt2}]: {result}\n')
            counter += 1
            cnt2 += 1
            if not result:
                print(test)
            #displacy.serve()