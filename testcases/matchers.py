from collections import abc
import numpy as np
import spacy
from rich import print
from spacy import displacy
from dependency_matchers import MatchersFactory
from data import Test,  nlp

VERBS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
IMPERATIVE_VERBS = ['VB', 'VBP']

def is_conditional_test(test:abc.Container) -> bool: #OK
    """
    1) It uses coordinating conjunctions, such as "and" or "or".
    2) Or uses a conditional "if".
    """
    matcher = MatchersFactory.conditional_test_matcher()
    for step in test.steps:
            matches = []
            action_matches = matcher(step.action)
            if action_matches:
                return True
    return False

def is_eager_step(test: abc.Container) -> bool: #OK!
    """
    More than one imperative verb per step
    """
    eager_step = 0
    steps = test.steps
    for step in steps:
        actions = [action for action in step.action if action.tag_ in IMPERATIVE_VERBS]
        eager_step = eager_step + len(actions)
    return eager_step > 1

def is_unverified_step(test: abc.Container) -> bool: #OK!
    """
    Missing verification step
    """
    steps = test.steps
    return len([step for step in steps if len(step.reactions) == 0]) > 0

def is_misplaced_precondition(test: abc.Container) -> bool:
    def get_tags(sentence) -> list:
        return [token.tag_ for token in sentence if token.tag_ in VERBS]
    actions = get_tags(test.steps[0].action)
    if not actions or actions[0] not in IMPERATIVE_VERBS:
        return True
    return False


def is_misplaced_step(test: abc.Container) -> bool:
    """
    Steps usually come on the imperative format. Imperative sentences usually start with a verb in second person.
    https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    This function checks if one of the steps of a test is an imperative sentence.
    """
    def has_imperative_sentence(doc: spacy.tokens.Doc) -> bool:
        for sentence in doc.sents:
            if sentence[0].tag_ in IMPERATIVE_VERBS:
                return True
        return False

    steps = test.steps
    marked_steps = [
        step for step in steps for reaction in step.reactions if has_imperative_sentence(reaction)]
    return len(marked_steps) > 0

def is_undefined_wait(test: abc.Container) -> bool:
    matcher = MatchersFactory.undefined_wait_matcher()
    for step in test.steps:
            matches = []
            action_matches = matcher(step.action)
            if action_matches:
                return True
    return False

def is_misplaced_result(test: abc.Container) -> bool:
    """
    Checks for active pronouns on the test.reaction field.

    A verification verb (check, verify, observe, recheck) in the step description
    Declarative sentence after any imperative one in the steps
    something (must verb) - verbos modais de obrigatoriedade devem entrar na classificação de verbos de verificação
    """

    matcher = MatchersFactory.misplaced_result_matcher()
    for step in test.steps:
        matches = []
        #first test
        action_matches = matcher(step.action)
        if action_matches:
            print(step.action)
            return True
        #Second test
        verbs = [token.tag_ for token in step.action if token.tag_ in VERBS]
        found_first = False
        for verb in verbs:
            if verb in IMPERATIVE_VERBS:
                found_first=True
            if found_first and verb not in IMPERATIVE_VERBS:
                return True
    return False

def is_vague_step(test: abc.Container) -> bool: #bad verification format
    """
    Pra Vague Step, olhar so os passos (actions) e procurar POS=ADJ && Tag=JJ #is_ambiguous_test
    """
    breakpoint()
    for step in test.steps:
        tag_pos = [[token.tag_ for token in step.action],[token.pos_ for token in step.reactions]]
        if tag_pos[1] in ['ADJ'] and tag_pos[0] in ['JJ']:
            return True
    return False

def is_vague_verification(test: abc.Container) -> bool:  #is_bad_verification_formatT
# There are more accurate methods which works even without the question mark egg: https://github.com/kartikn27/nlp-question-detection
# Pra Vague Verification, olhar só os resultados (reactions) e procurar (POS=ADJ && Tag=JJR) || (POS=ADV && Tag=RB)
    breakpoint()
    for step in test.step:
        tag_pos = [[token.tag_ for token in step.reactions],[token.pos_ for token in step.reactions]]
        if tag_pos[1] in ['ADJ'] and tag_pos[0] in ['JJR']:
            return True
        if tag_pos[1] in ['ADV'] and tag_pos[0] in ['RB']:
            return True
    return False

    # steps = test.steps
    # bad_verification_format_steps = [step for step in test if '?' in steps]
    # return len(bad_verification_format_steps) > 0
