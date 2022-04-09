from collections import abc
try:
    from rich import print
except ModuleNotFoundError:
    pass

from data import get_tests, smells_loader

import spacy

def is_unverified_step(test:abc.Container) -> bool:
    return len([i for i in test if len(i.reactions) == 0]) > 0


if __name__ == '__main__':
    #nlp = spacy.load('en_core_web_sm')
    tests = get_tests('ET')
    print(is_unverified_step(tests[0]))