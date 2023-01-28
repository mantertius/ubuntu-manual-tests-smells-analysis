from rich import print
from data import get_tests
import matchers

if __name__ == '__main__':
    # _in = input("Type the Manual Test Smell Acronym or the Posix Path:")
    # tests = get_tests(_in)

    tests = get_tests('PCAS')
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