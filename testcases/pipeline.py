import spacy
from collections import namedtuple

#TODO: Turn it into a singleton
nlp = spacy.load('en_core_web_lg')

Test = namedtuple('Test',['file','header','steps'])
Step = namedtuple('Step', ['action', 'reactions']) #Step([action],[reactions])