from cgi import test
from http.cookiejar import FileCookieJar
from importlib.resources import path
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

Test = namedtuple('Test',['file','header','step'])
Step = namedtuple('Step', ['action', 'reactions'])
#TODO #13 set the dataframe to not ignore headers

def smells_loader_closure():
    df = pd.read_csv('files.csv')
    df[SMELL_COL] = df[SMELL_COL].fillna('')
    df[SMELL_COL] = df[SMELL_COL].apply(lambda x: x.replace(' ', '').split(','))
    #df2 = pd.DataFrame(df[FILE_COL])
    #print(df2[FILE_COL])
    df[FILE_COL] = df[DIR_COL]+df[FILE_COL]
    df = df[[FILE_COL, SMELL_COL]]
    df = df.loc[df[FILE_COL].apply(lambda x: Path(x).exists())]
    df[FILE_COL] = df[FILE_COL].apply(lambda x: Path(x))

    def smells_loader(smell_acronym:str) -> pd.DataFrame:
        return df.loc[df[SMELL_COL].apply(lambda x: smell_acronym in x)].reset_index(drop=True)

    #TODO #14 find a way to display the name of the file that has the smell
    return smells_loader

smells_loader = smells_loader_closure()

def erase_split(text:str, erase:str, split:str):
    return [chunk for chunk in text.replace(erase,'').split(split) if chunk]

@singledispatch
def split_tests(text):
    pass

def split_tests(text:str):
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

def split_tests_steps(tests):
    result = []
    for test in tests:
        test = [erase_split(t, '</dd>', '<dd>') for t in test]
        test = [Step(pipeline(action), [pipeline(reaction) for reaction in reactions])
                    for action, *reactions in test
                ]
        result.append(test)
    return result

@singledispatch
def get_tests(arg):
    """
    Pass a str with the smell acronym to read all smells with that acronym;
    Pass a pathlib.PosixPath pointing to a smell file to read all smells within that file;
    """
    pass

@get_tests.register(str)
def _(smell_acronym:str):
    test_list = [test for path in smells_loader(smell_acronym)[FILE_COL] for test in split_tests(path.read_text())]
    path_list = [path for path in smells_loader(smell_acronym)[FILE_COL]]
    
    #print(path_list[0])
    return test_list, path_list

@get_tests.register(PosixPath)
def _(filepath:PosixPath):
    return split_tests(filepath.read_text())