from collections import abc, namedtuple
import re
import pandas as pd
NAME_COL = 'Summary'
PRECON_COL = 'Initial Condition'
STEPS_COL = 'Step Description'	
RESULTS_COL = 'Expected Results'

Test = namedtuple('Test',['name','header','steps'])
Step = namedtuple('Step',['action','reactions'])


def moto_loader_closure():
    df = pd.read_csv('moto_exp.csv')
    df = df.fillna('')
    df = df[[NAME_COL,PRECON_COL,STEPS_COL,RESULTS_COL]]
    print(df)
    return df.reset_index(drop=True)

def extract_texts(text:str) -> abc.Container:
    spaces = r'\s{2,}'
    breaks = r'\n'
    steps_number = r'\*Step \d\*'
    null = r'\*Step \d\* null'
    text = re.sub(re.compile(null), '', text)
    text = re.sub(re.compile(steps_number), '\n', text)
    text = re.sub(re.compile(breaks), '', text)
    text = re.sub(re.compile(spaces),' ', text)


if __name__ == '__main__':
    moto_loader_closure()