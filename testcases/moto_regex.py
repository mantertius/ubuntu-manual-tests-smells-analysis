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
    #print(df)
    return df.reset_index(drop=True)

def extract_texts(text:str) -> abc.Container:
    spaces = r'\s{2,}'
    breaks = r'\n'
    steps_number = r'\*\s*(step|Step)\s*\d+\*'
    null = r'\*\s*(step|Step)\s*\d+\* null\n?'
    breakpoint()
    text = re.sub(re.compile(null), '', text)
    text = re.split(re.compile(steps_number), '\n', text)
    text = re.sub(re.compile(breaks), '', text)
    text = re.sub(re.compile(spaces),' ', text)
    print(text)

if __name__ == '__main__':
    df = moto_loader_closure()
    text = '''*Step 1*
  1. Test on projects that support Wireless Charging (Reverse Charging)
  2. First time that Power Sharing is being used on DUT
  3. Mobile phone power is at least 20%
  4. Power sharing will be automatically disabled after 1 minute if isn't detect a device
*Step 2* null
*Step 2* null'''
    extract_texts(text)
        