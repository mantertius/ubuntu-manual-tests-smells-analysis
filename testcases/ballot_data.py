import logging.config
import re

import pandas as pd
from bs4 import BeautifulSoup

from pipeline import nlp, Step, Test

logging.config.fileConfig(fname='log.config', disable_existing_loggers=False)
log = logging.getLogger(__name__)

def split_test_case(tc_soup:BeautifulSoup) -> list:
    body = tc_soup.tbody
    steps = [step for step in body.find_all('tr') if len(step.find_all('td')) == 3] # Each step has 3 columns on the table
    test_case = tc_soup.find('th', attrs={'colspan': '4'}).text.strip()
    objective = _get_objective(tc_soup)
    preconditions = _get_preconditions(tc_soup)
    if not steps: #Test without steps
        return None
    header = steps[0]
    steps = steps[1::]
    header = [tag.text.strip() for tag in header.find_all('td')]
    steps  = [_clear_td(step) for step in steps]
    df = pd.DataFrame(steps,columns=header)
    df['test_case'] = test_case #Testcase name
    df['objective'] = objective
    df['preconditions'] = preconditions
    return df

def pipeline(list_of_dfs) -> list:
    '''Receives a list of dataFrames and returns a list of clean Tests after using some inside functions'''
    log.debug('Starting pipeline')
    def extract_texts(raw_text:str) -> list:
        '''Extracts texts from a string'''
        log.debug('Starting text extraction')
        pattern = r'\\{0,2}n{0,}\\t{0,}'
        breaks = r'\n{2,}'
        spaces = r'\s{2,}'
        text = re.sub(pattern, '\n', raw_text)
        text = re.sub(breaks, '\n', text)
        text = re.sub(spaces, ' ', text)
        return text


    def generate_Test(df:pd.DataFrame) -> Test:
        '''Creates a Test'''

        log.debug('Creating a new test')
        try:
            if df is not None:
                name = _pipeline(df['test_case'][0])
                header = _pipeline(df['preconditions'][0]) #estamos ignorando os objetivos
        except:
            log.error('Algo deu errado.')

        steps = list()

        for row in df.itertuples(index=False):
            action = _pipeline(row[1])
            reactions = _pipeline(row[2])
            step = Step(action,[reactions])
            steps.append(step)
        new_test = Test(file=name, header=header, steps=steps)
        log.debug('New test created')
        return new_test

    def _pipeline(raw_text:str):
        '''Recieves raw_text and returns clean_text as a Doc'''
        clean_text = extract_texts(raw_text)
        log.debug(f'Texts extracted. Passing nlp...')
        if not clean_text:
            return nlp('')
        if isinstance(clean_text,list) and len(clean_text) > 1:
            chunks = [nlp(element) for element in clean_text if len(clean_text) > 1]
        else:
            chunks = nlp(clean_text)
        return chunks

    all_tests = list()
    for df in list_of_dfs:
        '''Each df is a testcase.'''
        if df is not None:
            try:
                new_test = generate_Test(df)
                all_tests.append([new_test])
            except:
                log.error('FAIL.')
                break
    return all_tests


def parse_tests(soup:BeautifulSoup) -> list:
    log.debug('Start parsing.')
    tests = soup.find_all('table', attrs = {'class':'tc'})
    tests = [split_test_case(test) for test in tests if test]
    log.debug('Parsing successful')
    return tests

def _clear_td(td_soup:BeautifulSoup) -> list:
    result = td_soup.find_all('td')
    return [td.text.strip() for td in result]

def _get_objective(soup:BeautifulSoup) -> str:
    objective = [tag.text.strip() for tag in soup.find_all('td') if 'Objetivo do Teste' in tag.text.strip()]
    if objective:
        objective = objective[0]
    else:
        objective = ''
    return objective

def _get_preconditions(soup:BeautifulSoup) -> str:
    preconditions = [tag.text.strip() for tag in soup.find_all('td') if 'Pré-condições:' in tag.text]
    if preconditions:
        preconditions = preconditions[0]
    else:
        preconditions = ''
    return preconditions


def get_tests(smell_acronym:str) -> list:
    log.info('Start of Ballot retrieving...')
    try:
        with open('page.htm', 'r', encoding='utf8') as f:
            soup = BeautifulSoup(f, 'lxml')
    except FileNotFoundError:
        log.error('adicione o page.htm')
    tests = parse_tests(soup)
    tests = pipeline(tests)
    log.info('End of Ballot retrieving.')
    return tests
