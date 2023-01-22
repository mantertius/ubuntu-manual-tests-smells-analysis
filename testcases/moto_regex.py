from collections import abc, namedtuple
import re
import pandas as pd
from rich import print
import spacy

nlp = spacy.load('en_core_web_lg')

NAME_COL = 'Summary'
PRECON_COL = 'Initial Condition'
STEPS_COL = 'Step Description'	
RESULTS_COL = 'Expected Results'
SMELL_COL = 'How to detect?'

Test = namedtuple('Test',['name','header','steps'])
Step = namedtuple('Step',['action','reactions'])


def moto_smell_loader_closure():
    df = pd.read_csv('moto_exp.csv')
    df = df.fillna('')
    df = df[[NAME_COL, PRECON_COL, STEPS_COL, RESULTS_COL, SMELL_COL]]
    print(df)
    def smells_loader(smell_acronym: str) -> pd.DataFrame:
        if smell_acronym == '':
            return df.reset_index(drop=True)
        return df.loc[df[SMELL_COL].apply(lambda x: smell_acronym in x)].reset_index(drop=True)
    return smells_loader

smells_loader = moto_smell_loader_closure()


def moto_ambt():
    df = pd.read_csv('moto_exp.csv', index_col=False)
    df = df.fillna('')
    df = df[[NAME_COL, PRECON_COL, STEPS_COL, RESULTS_COL, SMELL_COL]]
    #print(df)
    #df = df.reset_index(drop=True)
    new_df = df[df['How to detect?'].str.contains('AmbT')]
    #print(new_df)
    new_df = new_df.reset_index(drop=True)
    new_df.rename(columns= {NAME_COL : 'NUMERO E NOME DO ARQUIVO', 'How to detect?' : 'QUAL SMELL?' }, inplace=True)
    new_df.to_csv('ambt_moto.csv')


def extract_texts(text:str) -> abc.Container:
    #print(text)
    spaces = r'\s{2,}'
    breaks = r'\n+'
    before_breaks = r'\s+\n+'
    steps_number = r'\*\s*(step|Step)\s*\d+\*\s*\n*'
    null = r'\*\s*(step|Step)\s*\d+\* null\n{0,}?'
    text = re.sub(re.compile(null), '', text)
    #print(text)
    text = re.split(re.compile(steps_number), text)
    stripped_text = [token.strip() for token in text if token and not token.isspace() and token != 'Step']
    print(stripped_text)
    #breakpoint()
    if stripped_text and len(stripped_text) == 1:
        if re.findall(r'\d+\.', stripped_text[0]): #type(stripped_text)== list and 
            stripped_text = re.split(r'\d+\. ',stripped_text[0])
    #print(f'This is the new text: {stripped_text}')

    # print(new_text)
    final_text = []
    for token in stripped_text:
        token = re.sub(re.compile(breaks), '', token)
        token = re.sub(re.compile(spaces),' ', token)
        if token != '':
            final_text.append(token.strip())
    # text = re.sub(re.compile(breaks), '', text)
    # text = re.sub(re.compile(spaces),' ', text)
    print('-----------------------------')
    print(text)
    print(f'This is the final text:{final_text}')
    if len(final_text) == 1:
        return final_text[0]
    if len(final_text) == 0:
        return None
    return final_text

def pipeline(raw_text:str) -> abc.Container:
    clean_text = extract_texts(raw_text)
    if clean_text == None:
        return None
    #print(clean_text)
    #breakpoint()
    if len(clean_text) > 1 and type(clean_text) == list:
        chunks = [nlp(element) for element in clean_text if len(clean_text) > 1]
    else:
        chunks = nlp(clean_text)   
    #print(chunks)
    return chunks
        
def get_tests(smell_acronym : str):
    df = smells_loader(smell_acronym)
    print(df)
    result = []
    for row in df.itertuples(name = 'Teste', index=False):
        name = row[0]
        print(name)
        header = pipeline(row[1])
        actions = pipeline(row[2])
        reactions = pipeline(row[3])
        temp = [Test(name= name, header=header, steps=Step(actions, reactions))]
        result.append(temp)
        # breakpoint()
    return result

def get_tests_from_name(test_name:str):
    df = smells_loader('')
    test_row = df.loc[df[NAME_COL].apply(lambda x: test_name in x)]
    result = []
    for row in test_row.itertuples(name = 'Teste', index=False):
        name = row[0]
        print(name)
        header = pipeline(row[1])
        actions = pipeline(row[2])
        reactions = pipeline(row[3])
        temp = [Test(name= name, header=header, steps=Step(actions, reactions))]
        result.append(temp)
        # breakpoint()
    return result

if __name__ == '__main__':
    df = moto_smell_loader_closure()
    result = get_tests('None')
    print(result)
    # rs = get_tests_from_name('TC - [Folio]-Turn on/off Folio when the screen is lock/Unlock')
    # print(rs)