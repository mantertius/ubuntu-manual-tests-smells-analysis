import re
from collections import namedtuple,abc
from bs4 import BeautifulStoneSoup, BeautifulSoup
import pandas as pd
from rich import print

Test = namedtuple('Test',['name','header','steps'])
Step = namedtuple('Step', ['action', 'reactions'])

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

def pipeline(list_of_dfs) -> Test:
    '''Receives a list of dataFrames and returns a list of clean Tests after using some inside functions'''
    def extract_texts(raw_text:str) -> list:
        pattern = r'\\{0,2}n{0,}\\t{0,}'
        breaks = r'\n{2,}'
        spaces = r'\s{2,}'
        text = re.sub(pattern, '\n', raw_text)
        text = re.sub(breaks, '\n', text)
        text = re.sub(spaces, ' ', text)
        print(text)~
        breakpoint()

    def generate_Test(df:pd.DataFrame) -> list:
        name =      extract_texts(df['test_case'])
        header =    extract_texts(df['preconditions']) #estamos ignorando os objetivos
        steps = list()
        actions = []
        reactions = []
        for row in df.itertuples(index=False):
            breakpoint()
            actions.append(extract_texts(row[1]))
            reactions.append(extract_texts(row[2]))
        new_Test = Test(name=name, header=header, steps = Step(action,reactions))

    for df in list_of_dfs:
        breakpoint()
        test:list = generate_Test(df)

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
    pass

if __name__ == '__main__':
    try:
        with open('page.htm', 'r') as f:
            soup = BeautifulSoup(f, 'lxml')
    except FileNotFoundError:
        print('You must add the tests html file on the path \'page.htm\'. This file is ignored via .gitignore')
    tests = parse_tests(soup)
    breakpoint()
    tests = pipeline(tests)