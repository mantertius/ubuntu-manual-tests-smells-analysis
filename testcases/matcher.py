import pandas as pd
from pathlib import Path
from collections import abc
import re
from rich import print

DIR_COL = 'DIRETÓRIO'
FILE_COL = 'NUMERO E NOME DO ARQUIVO'
SMELL_COL = 'QUAL SMELL?'

def smells_loader_closure():
    df = pd.read_csv('files.csv')
    df[SMELL_COL] = df[SMELL_COL].fillna('')
    df[SMELL_COL] = df[SMELL_COL].apply(lambda x: x.replace(' ', '').split(','))
    df[FILE_COL] = df[DIR_COL]+df[FILE_COL]
    df = df[[FILE_COL, SMELL_COL]]
    df = df.loc[df[FILE_COL].apply(lambda x: Path(x).exists())]
    df[FILE_COL] = df[FILE_COL].apply(lambda x: Path(x))

    def smells_loader(smell:str) -> pd.DataFrame:
        return df.loc[df[SMELL_COL].apply(lambda x: smell in x)].reset_index(drop=True)

    return smells_loader

def erase_split(text:str, erase:str, split:str):
    return [chunk for chunk in text.replace(erase,'').split(split) if chunk]

def split_tests(text:str) -> abc.Container[abc.Sequence]:
    spaces = r'\s{2,}'
    breaks = r'\n'
    trailing_whitespace = r'> '
    text = re.sub(re.compile(spaces),' ',text)
    text = re.sub(re.compile(breaks),' ',text)
    text = re.sub(re.compile(trailing_whitespace),'>',text)
    tags = r'(?<=<dl>)(.+?)(?=</dl>)'
    rr = re.compile(tags)
    tests = list(re.findall(tags,text))
    tests = [erase_split(r,'</dt>','<dt>') for r in tests]
    return tests


def split_tests_steps(tests:abc.Container[abc.Sequence]) -> abc.Container[abc.Sequence]:
    result = []
    for test in tests:
        test = [erase_split(t, '</dd>', '<dd>') for t in test]
        test = [(head, tail) for head, *tail in test]
        result.append(test)
    return result

if __name__ == '__main__':
    smells_loader = smells_loader_closure()
    df = smells_loader('EH')

    text = df[FILE_COL].iloc[0].read_text()
    r = split_tests(text)
    rr = split_tests_steps(r)
    print(rr)