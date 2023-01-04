import re
from glob import glob
from pathlib import Path, PosixPath
from collections import namedtuple, abc
from functools import singledispatch
from rich import print

import pandas as pd
import numpy as np
import spacy
from scipy.spatial import distance

nlp = spacy.load('en_core_web_lg')

DIR_COL = 'DIRETÓRIO'
FILE_COL = 'NUMERO E NOME DO ARQUIVO'
SMELL_COL = 'QUAL SMELL?'

Test = namedtuple('Test',['file','header','steps'])
Step = namedtuple('Step', ['action', 'reactions']) #Step([action],[reactions])


def smells_loader_closure():
    df = pd.read_csv('files.csv')           #lê o caminho dos dados
    df[SMELL_COL] = df[SMELL_COL].fillna('')
    df[SMELL_COL] = df[SMELL_COL].apply(lambda x: x.replace(' ', '').split(','))
    #df2 = pd.DataFrame(df[FILE_COL])
    #print(df2[FILE_COL])
    df[FILE_COL] = df[DIR_COL]+df[FILE_COL]
    df = df[[FILE_COL, SMELL_COL]]
    df = df.loc[df[FILE_COL].apply(lambda x: Path(x).exists())]
    df[FILE_COL] = df[FILE_COL].apply(lambda x: Path(x))
    
    def smells_loader(smell_acronym:str) -> pd.DataFrame:
        """
        Will return every filepath that has the smell_acronym. If no acronym is passed, returns all.
        """
        if smell_acronym != '':
            return df.loc[df[SMELL_COL].apply(lambda x: smell_acronym in x)].reset_index(drop=True) #this is a df of paths
        return df.reset_index(drop=True)

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

def expand_words(words, k=5) -> tuple:
    expanded_words = [k_closest_words(w, k) for w in words]
    print(f'{words}:{expanded_words}\n')
    return tuple(set([word.lower() for word_list in expanded_words for word in word_list]))

k_closest_words = k_closest_words_closure()

def erase_split(text:str, erase:str, split:str):
    return [chunk for chunk in text.replace(erase,'').split(split) if chunk]

@singledispatch
def split_tests(text, filepath:str):
    pass

def extract_texts(text:str, filepath:str) -> abc.Container:
    """
    Gets the raw text from the filepath as well the filepath as a string and returns a list containing the parsed raw texts from the tests.
    """
    spaces = r'\s{2,}'
    breaks = r'\n'
    trailing_whitespace = r'> '

    test_title = r'(?<=<strong>)(.+?)(?=</strong>)'
    test_header = r'(?<=^)(.+?)(?=<dl>)|(?<=</dl>)(.+?)(?=<dl>)' #it's the title and the preconditions
    comments = r'(?<=<!--)(.+?)(?=-->)'
    tags = r'(?<=<dl>)(.+?)(?=</dl>)'
    language_disclaimer = r'(?<=<em>)(.+?)(?=</em>)'

    text = re.sub(re.compile(language_disclaimer),'',text)
    text = re.sub(re.compile(comments),' ',text)
    text = re.sub(re.compile(spaces),' ',text)
    text = re.sub(re.compile(breaks),' ',text)
    text = re.sub(re.compile(trailing_whitespace),'>',text)

    mid_header = r'(?<=<\/dl>)(.+?)(?=<dl>)'
    init_header = r'(?<=^)(.+?)(?=<dl>)'

    headers1 = list(re.findall(init_header,text))
    headers2 = list(re.findall(mid_header,text))

    headers = headers1+headers2#TODO  #17   #talvez seja necessário usar erase_split() em headers2 para que a gente consiga pegar o caso de >=3 testes no arquivo
    headers = [remove_html(header) for header in headers]

    tests = list(re.findall(tags,text)) #textão único, juntando tudo que tá dentro de <dl>
    tests = [erase_split(text=r,erase='</dt>',split='<dt>') for r in tests] #separa cada grupo formado por [passo e steps] dos outros [passo e steps]
    return tests, headers

def split_tests(text:str, filepath:str) -> Test:
    tests, headers = extract_texts(text, filepath)
    tests = split_tests_steps(tests)

    result = []
    for test in tests:
        temp = [Test(file=filepath,header=[header for header in headers],steps=[steps for steps in test])]
        result.append(temp)
    return result

def pipeline(text:str) -> str:
    result = remove_html(text)
    return nlp(result)

def remove_html(text:str):
    remove_html = re.compile('<.*?>')
    result = re.sub(remove_html, '', text)
    return result

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
    test_list = [test for path in smells_loader(smell_acronym)[FILE_COL]
                        for test in split_tests(path.read_text(encoding='utf-8'),path)]
    return test_list

@get_tests.register(PosixPath)
def _(filepath:PosixPath):
    return split_tests(filepath.read_text(encoding='utf-8'), filepath)



#Percebi que o objeto nlp.vocab não vai conseguir ser visualizado pelas funçoes matcher_ (será? nlp é variável global). Não sei como resolver de um jeito bonito. Talvez o singleton?

def on_match(matcher, doc, id, matches):
    for match_id, start, end in matches:
        span = doc[start:end]
        string_id = nlp.vocab.strings[match_id]
        print(f'[{string_id}]:{span.text}')

def matcher_maker(test, pattern_name, pattern):
    """
    DEPRECATED
    Recieves the subject, the pattern_name and the pattern. Returns the number of matches.
    """
    matcher = spacy.matcher.Matcher(nlp.vocab)
    matcher.add(pattern_name, [pattern], on_match=on_match)
    matches = matcher(test)
    return matches

def matcher_wait(test):
    """DEPRECATED"""
    pattern = [{'LOWER': {"IN" : ["wait","halt","rest","holdup","stay on hold"]}}, {'POS' : 'ADP', 'OP' : '+'} , {'LIKE_NUM' : False}]
    number_of_waits_without_num = len(matcher_maker(test,"NOT_NUM",pattern))
    return number_of_waits_without_num

def matcher_if(test):
    """DEPRECATED"""

    pattern = [{'LOWER': {"IN":['if','whether','depending','when','in case']}}]
    number_of_ifs = len(matcher_maker(test,"HAS_IF",pattern))
    return number_of_ifs

def matcher_optional(test):
    """DEPRECATED"""
    pattern = [{'LOWER':"optional"}]
    matches = matcher_maker(test,"HAS_OPTIONAL", pattern)
    number_of_optionals = len(matches)
    return number_of_optionals

def matcher_pre_condition(test):
    """DEPRECATED"""
    # i thinks this pattern is too embracing, it may get false positives.
    pattern = [{'LOWER':{"IN" : ["make sure", "make certain","see to it","secure","guarantee","warrant",'certify','set the seal on', 'clinch', 'confirm', 'check','verify', 'corroborate', 'establish', 'sew up', 'ensure']}}]
    matches = matcher_maker(test,"HAS_MISPLACED_PRE_CONDITION",pattern)
    number_of_misplaced_pre_conditions = len(matches)
    return number_of_misplaced_pre_conditions
