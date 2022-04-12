import pandas as pd
from pathlib import Path, PosixPath
from collections import abc
import re
from collections import namedtuple
from functools import singledispatch
import spacy

nlp = spacy.load('en_core_web_sm')

DIR_COL = 'DIRETÓRIO'
FILE_COL = 'NUMERO E NOME DO ARQUIVO'
SMELL_COL = 'QUAL SMELL?'

Step = namedtuple('Step', ['action', 'reactions'])

def smells_loader_closure():
    df = pd.read_csv('files.csv')
    df[SMELL_COL] = df[SMELL_COL].fillna('')
    df[SMELL_COL] = df[SMELL_COL].apply(lambda x: x.replace(' ', '').split(','))
    df[FILE_COL] = df[DIR_COL]+df[FILE_COL]
    df = df[[FILE_COL, SMELL_COL]]
    df = df.loc[df[FILE_COL].apply(lambda x: Path(x).exists())]
    df[FILE_COL] = df[FILE_COL].apply(lambda x: Path(x))

    def smells_loader(smell_acronym:str) -> pd.DataFrame:
        return df.loc[df[SMELL_COL].apply(lambda x: smell_acronym in x)].reset_index(drop=True)

    return smells_loader

smells_loader = smells_loader_closure()

def erase_split(text:str, erase:str, split:str):
    return [chunk for chunk in text.replace(erase,'').split(split) if chunk]

@singledispatch
def split_tests(text) -> abc.Container[abc.Sequence]:
    pass

def split_tests(text:str) -> abc.Container[abc.Sequence]:
    spaces = r'\s{2,}'
    breaks = r'\n'
    trailing_whitespace = r'> '
    text = re.sub(re.compile(spaces),' ',text)
    text = re.sub(re.compile(breaks),' ',text)
    text = re.sub(re.compile(trailing_whitespace),'>',text)
    tags = r'(?<=<dl>)(.+?)(?=</dl>)'
    tests = list(re.findall(tags,text))
    tests = [erase_split(r,'</dt>','<dt>') for r in tests]
    tests = split_tests_steps(tests)
    return tests

def pipeline(text:str) -> str:
    remove_html = re.compile('<.*?>')
    result = re.sub(remove_html, '', text)
    return nlp(result)

def split_tests_steps(tests:abc.Container[abc.Sequence]) -> abc.Container[abc.Sequence]:
    result = []
    for test in tests:
        test = [erase_split(t, '</dd>', '<dd>') for t in test]
        test = [Step(pipeline(action), [pipeline(reaction) for reaction in reactions])
                    for action, *reactions in test
                ]
        result.append(test)
    return result

@singledispatch
def get_tests(arg) -> abc.Container[abc.Container]:
    """
    Pass a str with the smell acronym to read all smells with that acronym;
    Pass a pathlib.PosixPath pointing to a smell file to read all smells within that file;
    """
    pass

@get_tests.register(str)
def _(smell_acronym:str) -> abc.Container[abc.Container]:
    return [test for path in smells_loader(smell_acronym)[FILE_COL]
                    for test in split_tests(path.read_text())
            ]

@get_tests.register(PosixPath)
def _(filepath:PosixPath) -> abc.Container[abc.Container]:
    return split_tests(filepath.read_text())