import re
from collections import abc, namedtuple
from functools import singledispatch
from http.cookiejar import FileCookieJar
from pathlib import Path, PosixPath

import numpy as np
import pandas as pd
import spacy
from scipy.spatial import distance

nlp = spacy.load('en_core_web_lg')
nlp = spacy.load('pt_core_news_lg')


DIR_COL = 'DIRETÓRIO'
FILE_COL = 'NUMERO E NOME DO ARQUIVO'
SMELL_COL = 'QUAL SMELL?'

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

def k_closest_words_closure():
    vocab_ids = [x for x in nlp.vocab.vectors.keys()]
    vocab_vectors = np.array([nlp.vocab.vectors[x] for x in vocab_ids])
    def k_closest_words(input_word:str, k:int):
        input_word_vector = np.array([nlp.vocab[input_word].vector])
        # closest_indexes = distance.cdist(input_word_vector, vocab_vectors, metric='cosine').argsort()[0][:k]
        closest_indexes = distance.cdist(input_word_vector, vocab_vectors).argsort()[0][:k]
        return [nlp.vocab[vocab_ids[idx]].text for idx in closest_indexes]
    return k_closest_words

def expand_unispecific_words(unspecific_words = None, k=5) -> bool:
    if not unspecific_words:
        unspecific_words = ('all', 'default', 'any', 'some')
    unspecific_words = [k_closest_words(w, k) for w in unspecific_words]
    unspecific_words = tuple(set([word.lower() for word_list in unspecific_words for word in word_list]))
    return unspecific_words

k_closest_words = k_closest_words_closure()

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
    return [test for path in smells_loader(smell_acronym)[FILE_COL]
                    for test in split_tests(path.read_text())
            ]

@get_tests.register(PosixPath)
def _(filepath:PosixPath):
    return split_tests(filepath.read_text())
