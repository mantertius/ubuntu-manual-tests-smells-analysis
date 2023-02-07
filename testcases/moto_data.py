from collections import abc, namedtuple
import re
import pandas as pd
from rich import print
import spacy

from pipeline import nlp, Step, Test

NAME_COL = 'Summary'
PRECON_COL = 'Initial Condition'
STEPS_COL = 'Step Description'
RESULTS_COL = 'Expected Results'
SMELL_COL = 'How to detect?'


def moto_smell_loader_closure():
    df = pd.read_csv('moto_exp.csv')
    df = df.fillna('')
    df = df[[NAME_COL, PRECON_COL, STEPS_COL, RESULTS_COL, SMELL_COL]]

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
    new_df = df[df['How to detect?'].str.contains('AmbT')]

    new_df = new_df.reset_index(drop=True)
    new_df.rename(columns= {NAME_COL : 'NUMERO E NOME DO ARQUIVO', 'How to detect?' : 'QUAL SMELL?' }, inplace=True)
    new_df.to_csv('ambt_moto.csv')


def extract_texts(text:str) -> abc.Container:
    spaces = r'\s{2,}'
    breaks = r'\n+'
    before_breaks = r'\s+\n+'
    steps_number = r'\*\s*(step|Step)\s*\d+\*\s*\n*'
    null = r'\*\s*(step|Step)\s*\d+\* null\n{0,}?'
    text = re.sub(re.compile(null), '', text)

    text = re.split(re.compile(steps_number), text)
    stripped_text = [token.strip() for token in text if token and not token.isspace() and token != 'Step']

    if stripped_text and len(stripped_text) == 1:
        if re.findall(r'\d+\.', stripped_text[0]): #type(stripped_text)== list and
            stripped_text = re.split(r'\d+\. ',stripped_text[0])

    final_text = []
    for token in stripped_text:
        token = re.sub(re.compile(breaks), '', token)
        token = re.sub(re.compile(spaces),' ', token)
        if token != '':
            final_text.append(token.strip())
    if len(final_text) == 1:
        return final_text[0]
    elif len(final_text) == 0:
        return None
    return final_text

def pipeline(raw_text:str) -> abc.Container:
    clean_text = extract_texts(raw_text)
    if not clean_text:
        return None
    if isinstance(clean_text, list) and len(clean_text) > 1:
        chunks = [nlp(element) for element in clean_text if len(clean_text) > 1]
    else:
        chunks = [nlp(clean_text)]
    return chunks

def pipeline_reactions(reactions_raw_text:str) -> list:
    regex = re.compile(r'(\*.+\*)')
    splits = [split for split in regex.split(reactions_raw_text) if split]
    action_identifiers = [int(re.compile('\d+').findall(key)[0]) for key in splits[0:-1:2]]
    reactions = [nlp(reaction.strip()) for reaction in splits[1::2]]
    paired_reactions = dict(zip(action_identifiers,reactions))
    result = list()
    for action_number in action_identifiers:
        if (current_reaction := paired_reactions.get(action_number)):
            #breakpoint()
            result.append(current_reaction)
        else:
            result.append('')
    return result

# def _pipeline_reactions_nlp(reactions_list:list) ->


def get_tests(smell_acronym : str):
    df = smells_loader(smell_acronym)
    result = []
    # df = df.head(1)
    for row in df.itertuples(name = 'Teste', index=False):
        test_have_substeps = has_substeps(row[2]) and has_substeps(row[3])
        if not test_have_substeps:
            name = row[0]
            header = pipeline(row[1])
            actions = pipeline(row[2])
            reactions = pipeline_reactions(row[3])
            assert isinstance(actions[0], spacy.tokens.Doc)
            assert isinstance(reactions[0], spacy.tokens.Doc)
            steps = list()
            for (action, reaction) in zip(actions, reactions):
                step = Step(action, [reaction])
                assert isinstance(step.reactions, list)
                steps.append(step)
            test = Test(file=name, header=header, steps=steps)
            result.append([test])
    return result

def has_substeps(action_or_reaction:str) -> bool:
    substep_marker = re.compile('\n\W*\d+\.\s*\w+')
    return len(substep_marker.findall(action_or_reaction)) > 0

if __name__ == '__main__':
    # df = moto_smell_loader_closure()
    result = get_tests('')

    # rs = get_tests_from_name('TC - [Folio]-Turn on/off Folio when the screen is lock/Unlock')
