import spacy
from collections import namedtuple
import logging

log = logging.getLogger(__name__)
#TODO: Turn it into a singleton
SM = 'en_core_web_sm'
TRF = 'en_core_web_trf'
nlp = spacy.load(SM)
lang = nlp.meta['lang']
name = nlp.meta['name']
model_name = lang + '_' + name
log.info(f'spaCy model: {model_name}')
try:
    nlp_pt = spacy.load('pt_core_news_lg')
except OSError:
    log.error('Instale o modelo:\npython -m spacy download pt_core_news_lg')

Test = namedtuple('Test',['file','header','steps'])
Step = namedtuple('Step', ['action', 'reactions']) #Step([action],[reactions])
