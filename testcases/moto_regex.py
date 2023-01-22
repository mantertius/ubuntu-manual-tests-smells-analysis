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
    steps_number = r'\*\s*(step|Step)\s*\d+\*\s*\n*'
    null = r'\*\s*(step|Step)\s*\d+\* null\n{0,}?'
    text = re.sub(re.compile(null), '', text)
    #print(text)
    text = re.split(re.compile(steps_number), text) 
    #breakpoint()
    stripped_text = [token.strip() for token in text if token and not token.isspace() and token != 'Step']
    #print(f'This is the new text: {stripped_text}')

    # print(new_text)
    final_text = []
    for token in stripped_text:
        token = re.sub(re.compile(breaks), '', token)
        token = re.sub(re.compile(spaces),' ', token)
        final_text.append(token)
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

if __name__ == '__main__':
    df = moto_smell_loader_closure()
#     text = '''*Step 1*
#   1. Test on projects that support Wireless Charging (Reverse Charging)
#   2. First time that Power Sharing is being used on DUT
#   3. Mobile phone power is at least 20%
#   4. Power sharing will be automatically disabled after 1 minute if isn't detect a device
# *Step 2* null
# *Step 2* null'''
#     extract_texts(text)#moto_ambt()
    result = get_tests('AmbT')
    print(result)