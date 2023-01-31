import re
from collections import namedtuple,abc
from bs4 import BeautifulStoneSoup, BeautifulSoup
import pandas as pd
from rich import print

from pipeline import nlp, Step, Test



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

    def sync_df(unsynced_df) -> pd.DataFrame:
        df = pd.read_csv('box.csv')
        df = df[['NÚMERO','QUAL SMELL?']]
        for row in unsynced_df:
            if df[[]]

    breakpoint()
    df['QUAL SMELL?'] = new_df[]
    return df

def pipeline(list_of_dfs) -> list:
    '''Receives a list of dataFrames and returns a list of clean Tests after using some inside functions'''
    def extract_texts(raw_text:str) -> list:
        '''Extracts texts from a string'''
        pattern = r'\\{0,2}n{0,}\\t{0,}'
        breaks = r'\n{2,}'
        spaces = r'\s{2,}'
        text = re.sub(pattern, '\n', raw_text)
        text = re.sub(breaks, '\n', text)
        text = re.sub(spaces, ' ', text)
        return text
        #print(text)
        #breakpoint()

    def generate_Test(df:pd.DataFrame) -> Test:
        '''Creates a Test'''
        # breakpoint()
        try:
            if df is not None:
                name = _pipeline(df['test_case'][0])
                header = _pipeline(df['preconditions'][0]) #estamos ignorando os objetivos
        except:
            breakpoint()
        steps = list()
        # try:
        for row in df.itertuples(index=False):
            #breakpoint()
            action = _pipeline(row[1])
            reactions = _pipeline(row[2])
            step = Step(action,reactions)
            steps.append(step)
        new_Test = Test(file=name, header=header, steps = steps)
        return new_Test
    # except:
    def _pipeline(raw_text:str):
        '''Recieves raw_text and returns clean_text as a Doc'''
        clean_text = extract_texts(raw_text)
        print('.', end='')
        #reakpoint()
        if not clean_text:
            return None
        if isinstance(clean_text,list) and len(clean_text) > 1:
            chunks = [nlp(element) for element in clean_text if len(clean_text) > 1]
        else:
            chunks = nlp(clean_text)
        return chunks

    all_Tests = list()
    for df in list_of_dfs:
        '''Each df is a testcase.'''
        if df is not None:
            #print(f'Esse é o df: {df}')
            try:
                new_Test = generate_Test(df)
                all_Tests.append(new_Test)
                # breakpoint()
            except:
                print('FAIL.')
                break
    #print(COUNTER)
    return all_Tests


def parse_tests(soup:BeautifulSoup) -> list:
    tests = soup.find_all('table', attrs = {'class':'tc'})
    tests = [split_test_case(test) for test in tests if test]
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
    #TODO: integrar a análise feita em manual_test_smells.csv na lista de tests, somente desse jeito será possível acessar por classificação.

    pass

if __name__ == '__main__':
    try:
        with open('page.htm', 'r') as f:
            soup = BeautifulSoup(f, 'lxml')
    except FileNotFoundError:
        print('You must add the tests html file on the path \'page.htm\'. This file is ignored via .gitignore')
    tests = parse_tests(soup)
    tests = pipeline(tests)
    # for test in tests:
    #     if test is not None:
    #         print(test)
    #     else:
    #         print('')
    #breakpoint()