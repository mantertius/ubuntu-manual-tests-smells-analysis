import logging.config

from data import get_tests
from testcases import matchers

logging.config.fileConfig(fname='log.config', disable_existing_loggers=False)
log = logging.getLogger(__name__)

if __name__ == '__main__':
    log.info('Retrieving tests...')  # logging.info
    tests = get_tests('')  # lista com todos os testes

    log.info('Analyzing...')
    for (file_index, test_file) in enumerate(tests):
        for (test_index, test) in enumerate(test_file):
            matchers.find_conditional_test_logic(test_index, test)
            matchers.find_eager_step(test_index, test)
            matchers.find_unverified_step(test_index, test)
            matchers.find_misplaced_precondition(test_index, test)
            matchers.find_misplaced_step(test_index, test)
            matchers.find_misplaced_result(test_index, test)
            matchers.find_ambiguous_test(test_index, test)

    log.info('Analysis complete!')

    # Pro artigo:
    # PS1: Não há unverified step na urna
    # PS2: Não há misplaced precondition na urna
    # PS3: Em ambiguous tests, a urna só pega 'verb + indefinite determiner' e 'indefinite pronoun'. Tipos de
    # advérbios e de adjetivos não são reconhecidos pelo modelo em pt
    # PS4: Para Conditional Test Logic, estabelecer que a regra é a presença de cláusulas subordinadas (que representam
    # a condição a ser satisfeita). No entanto, o Spacy não oferece a divisão de cláusulas (independente e subordinada)
    # de uma sentença. Assim, nossa implementação ficou limitada à identificação de conjunções subordinativas no início
    # da sentença.

