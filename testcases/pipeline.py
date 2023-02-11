import sys

import spacy
from collections import namedtuple
import logging

log = logging.getLogger(__name__)

# TODO: Turn it into a singleton

try:
    if sys.argv[1] == 'portuguese':
        model = 'pt_core_news_lg'
    else:
        model = 'en_core_web_trf'
except IndexError:
    model = 'en_core_web_sm'  # Development only

nlp = spacy.load(model)

lang = nlp.meta['lang']
name = nlp.meta['name']
model_name = lang + '_' + name
log.info(f'spaCy model: {model_name}')

Test = namedtuple('Test', ['file', 'header', 'steps'])
Step = namedtuple('Step', ['action', 'reactions'])
