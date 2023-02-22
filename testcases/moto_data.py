import logging
import re

import pandas as pd

log = logging.getLogger(__name__)
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
    new_df.rename(columns={NAME_COL: 'NUMERO E NOME DO ARQUIVO', 'How to detect?': 'QUAL SMELL?'}, inplace=True)
    new_df.to_csv('ambt_moto.csv')


def normalize_text(text: str) -> str:
    text = re.sub(re.compile(r'null'), '', text)  # null
    text = re.sub(re.compile(r'\n+'), '', text)  # breaks
    text = re.sub(re.compile(r'\-\-\>'), ' -> ', text)  # menu_item1
    text = re.sub(re.compile(r'\s\>'), ' -> ', text)  # menu_item2
    text = re.sub(re.compile(r'\s{2,}'), ' ', text)  # spaces
    return text


def pipeline_steps(steps_raw_text: str) -> dict:
    regex = re.compile(r'(\*.+\*)')
    splits = [split for split in regex.split(steps_raw_text) if split]
    step_numbers = [int(re.compile(r'\d+').findall(key)[0]) for key in splits[0:-1:2]]
    steps = [step for step in splits[1::2]]
    paired_step_numbers = zip(step_numbers, steps)

    step_list = dict()
    for i in range(max(step_numbers)):
        step_list[i] = ''

    for index, step in paired_step_numbers:
        step_list[index - 1] += ' ' + normalize_text(step)
        step_list[index - 1] = step_list[index - 1].strip()

    return step_list


def get_tests(smell_acronym: str):
    log.info('Start of Moto retrieving...')
    df = smells_loader(smell_acronym)
    result = []
    for row in df.itertuples(name='Teste', index=False):
        test_have_substeps = has_substeps(row[2]) and has_substeps(row[3])
        if not test_have_substeps:
            name = row[0]
            header = ''  # not actually in use, would be row[2]
            actions = pipeline_steps(row[2])
            reactions = pipeline_steps(row[3])
            steps = list()
            for step, description in actions.items():
                if step in reactions and reactions[step] != '':
                    step = Step(nlp(description), [nlp(reactions[step])])
                else:
                    step = Step(nlp(description), [])
                steps.append(step)
            test = Test(file=name, header=header, steps=steps)
            result.append([test])
    log.info('End of Moto retrieving.')
    return result


def has_substeps(action_or_reaction: str) -> bool:
    substep_marker = re.compile('\n\W*\d+\.\s*\w+')
    return len(substep_marker.findall(action_or_reaction)) > 0
