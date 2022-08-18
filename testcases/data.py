from importlib.resources import path
import math
import pandas as pd
from pathlib import Path, PosixPath
from collections import abc
import re
from collections import namedtuple
from functools import singledispatch
from rich import print
import spacy

nlp = spacy.load('en_core_web_sm')

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
        Will return every filepath that has the smell_acronym.
        """
        return df.loc[df[SMELL_COL].apply(lambda x: smell_acronym in x)].reset_index(drop=True) #this is a df of paths 
    
    return smells_loader

smells_loader = smells_loader_closure()

def erase_split(text:str, erase:str, split:str):
    return [chunk for chunk in text.replace(erase,'').split(split) if chunk]

@singledispatch
def split_tests(text, filepath:str):
    pass

def split_tests(text:str, filepath:str) -> Test:
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
    #headers = [header for header in headers if header != '' for header_inside in header if header_inside != '']
    headers = [remove_html(header) for header in headers]

    tests = list(re.findall(tags,text)) #textão único, juntando tudo que tá dentro de <dl>
    tests = [erase_split(text=r,erase='</dt>',split='<dt>') for r in tests] #separa cada grupo formado por [passo e steps] dos outros [passo e steps]
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
    #breakpoint()
    #path = PosixPath('packages/SMELLY - 1677_GDebi')
    #testing = split_tests(path.read_text(), path)
    #breakpoint()
    ##test for path in smells_loader(smell_acronym)[FILE_COL] → test  #me dá a lista de todos os paths que tem o smell que eu pedi na variavel test

    #path_list = [path for path in smells_loader(smell_acronym)[FILE_COL]]
    
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
    Recieves the subject, the pattern_name and the pattern. Returns the number of matches.
    """
    matcher = spacy.matcher.Matcher(nlp.vocab)
    matcher.add(pattern_name, [pattern], on_match=on_match)
    matches = matcher(test)
    return matches

def matcher_wait(test):
    pattern = [{'LOWER': {"IN" : ["wait","halt","rest","holdup","stay on hold"]}}, {'POS' : 'ADP', 'OP' : '+'} , {'LIKE_NUM' : False}]
    number_of_waits_without_num = len(matcher_maker(test,"NOT_NUM",pattern))
    return number_of_waits_without_num

def matcher_if(test):
    pattern = [{'LOWER': {"IN":['if','whether','depending','when','in case']}}]
    number_of_ifs = len(matcher_maker(test,"HAS_IF",pattern))
    return number_of_ifs

def matcher_optional(test):
    pattern = [{'LOWER':"optional"}]
    matches = matcher_maker(test,"HAS_OPTIONAL", pattern)
    number_of_optionals = len(matches)
    return number_of_optionals

def matcher_pre_condition(test):
    # i thinks this pattern is too embracing, it may get false positives.
    pattern = [{'LOWER':{"IN" : ["make sure", "make certain","see to it","secure","guarantee","warrant",'certify','set the seal on', 'clinch', 'confirm', 'check','verify', 'corroborate', 'establish', 'sew up', 'ensure']}}]
    matches = matcher_maker(test,"HAS_MISPLACED_PRE_CONDITION",pattern)
    number_of_misplaced_pre_conditions = len(matches)
    return number_of_misplaced_pre_conditions


