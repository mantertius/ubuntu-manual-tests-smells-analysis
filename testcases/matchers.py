from collections import abc
import numpy as np
import spacy
from rich import print
from spacy import displacy
from matchers_factory import MatchersFactory
from data import Test, nlp
from keywords import Keywords
from csv_writter import resultsWritter
from spacy.tokens import Doc
from data import Test, nlp
import pandas as pd

VERBS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
IMPERATIVE_VERBS = ['VB', 'VBP']


def find_conditional_test_logic(index: int, test: abc.Container):
    """
    Subordinate (dependent clauses). They start with a subordinating conjunction
    """
    matcher = MatchersFactory.conditional_test_matcher()

    for step in test.steps:
        # Steps
        doc = nlp(step.action)
        for sentence in doc.sents:  # Analyze individual sentences, not the entire step text
            action_matches = matcher(sentence)
            for match_id, start, end in action_matches:
                span = sentence[start:end]
                resultsWritter().write(
                    [test.file, index, 'Conditional Test Logic', 'dependent clause', 'step', span, sentence])

        # Verifications
        for reaction in step.reactions:
            doc = nlp(reaction)
            for sentence in doc.sents:
                reaction_matches = matcher(sentence)
                for match_id, start, end in reaction_matches:
                    span = sentence[start:end]
                    resultsWritter().write(
                        [test.file, index, 'Conditional Test Logic', 'dependent clause', 'verification', span,
                         sentence])


def find_eager_step(index: int, test: abc.Container):
    """
    More than one imperative verb per step
    """
    steps = test.steps
    for step in steps:
        actions = [action for action in step.action if action.tag_ in IMPERATIVE_VERBS]
        if len(actions) > 1:
            resultsWritter().write([test.file, index, 'Eager Step', '', 'step', actions, step.action])


def find_unverified_step(index: int, test: abc.Container):
    """
    Missing verification step
    """
    steps = test.steps
    unverified_steps = [step for step in steps if len(step.reactions) == 0]
    for step in unverified_steps:
        resultsWritter().write([test.file, index, 'Unverified Step', '', 'step', '', step.action])


def find_misplaced_precondition(index: int, test: abc.Container):
    """
        Unverified steps, at the beginning of the test, that declare SUT state (e.g. 'wifi is turned off')
    """

    def get_first_unverified_steps() -> list:
        first_unverified_steps = []
        for step in test.steps:
            if step.reactions:
                break
            else:
                first_unverified_steps.append(step)
        return first_unverified_steps

    matcher = MatchersFactory.misplaced_precondition_matcher()
    unverified_steps = get_first_unverified_steps()
    for step in unverified_steps:
        action_matches = matcher(step.action)
        if action_matches:
            for match_id, token_ids in action_matches:
                ind_mood_verb = [token_id for token_id in token_ids if "Mood=Ind" in str(step.action[token_id].morph)]
                if ind_mood_verb:
                    words = [step.action[token_id] for token_id in sorted(token_ids)]
                    resultsWritter().write([test.file, index, 'Misplaced Precondition', '', 'step', words, step.action])


# def is_bad_verification_format(test: abc.Container) -> bool:  # BAD VERIFICATION FORMAT
#     # There are more accurate methods which works even without the question mark egg: https://github.com/kartikn27/nlp-question-detection
#     steps = test.steps
#     bad_verification_format_steps = [step for step in test if '?' in steps]
#     return len(bad_verification_format_steps) > 0


def find_misplaced_step(index: int, test: abc.Container):
    """
    Steps usually come on the imperative format. Imperative sentences usually start with a verb in second person.
    https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    This function checks if one of the steps of a test is an imperative sentence.
    """
    for step in test.steps:
        for reaction in step.reactions:
            for sentence in reaction.sents:
                token = sentence[0]
                if token.tag_ in IMPERATIVE_VERBS and token.text.lower() not in Keywords().keywords['verifications']:
                    resultsWritter().write(
                        [test.file, index, 'Misplaced Step', '', 'verification', token.text, reaction])


# def is_undefined_wait(test: abc.Container) -> bool:
#     matcher = MatchersFactory.undefined_wait_matcher()
#     for step in test.steps:
#         matches = []
#         action_matches = matcher(step.action)
#         if action_matches:
#             return True
#     return False


def find_misplaced_result(index: int, test: abc.Container):
    """
    A verification verb (check, verify, observe, recheck) in the step description
    Interrogative sentences as steps
    Declarative sentence after any imperative one in all steps
    """

    def get_root(doc: Doc) -> list:
        return [token.tag_ for token in doc if token.dep_ == 'ROOT']

    def is_imperative_sentence(sent: Doc) -> bool:
        root = get_root(sent)
        return root[0] in IMPERATIVE_VERBS

    def is_interrogative_sentence(sent: Doc) -> bool:
        return sent[-1].text == '?'

    matcher = MatchersFactory.misplaced_result_verification_matcher()
    for step in test.steps:
        # First test: A verification verb (check, verify, observe, recheck) in the step description
        action_matches = matcher(step.action)
        for match_id, token_ids in action_matches:
            for token_id in token_ids:
                resultsWritter().write(
                    [test.file, index, 'Misplaced Result', 'verification performed', 'step', step.action[token_id],
                     step.action])

        # Second test: Interrogative sentences as step
        for sentence in step.action.sents:
            if is_interrogative_sentence(sentence):
                resultsWritter().write(
                    [test.file, index, 'Misplaced Result', 'question as step', 'step', '', sentence])

    # Third test: Declarative sentence after any imperative one considering all steps
    matcher = MatchersFactory.misplaced_result_affirmative_sentences()
    verified_steps = [step for step in test.steps if step.reactions]
    for step in verified_steps:
        for sentence in step.action.sents:
            if not (is_interrogative_sentence(sentence) or is_imperative_sentence(sentence)):
                action_matches = matcher(sentence)
                for match_id, token_ids in action_matches:
                    words = [sentence[token_id] for token_id in sorted(token_ids)]
                    resultsWritter().write(
                        [test.file, index, 'Misplaced Result', 'SUT state declaration', 'step', words, sentence])


# def all_at_once_at_the_same_time(test: abc.Container) -> df:
#     df = pd.DataFrame()
#     breakpoint()
#     df["File/Testcase"] = test.file
#     cond_result, cond_match = is_conditional_test(test)
#     df['Conditional Test Logic'] = cond_result
#     df['Undefined Wait'] = wait_result
#     df['Misplaced Result'] = mis_result_result
#     df['Misplaced Pre-Condition'] = mis_precon_result
#     df['Eager Step'] =
#     df['Unverified Step']
#     df['Eager Step']


def find_ambiguous_test(index: int, test: abc.Container):
    """
        Comparative adverbs (RBR)
        Adverbs of manner(RB)
        Comparative and superlative adjectives (JJR, JJS)
        Indefinite pronouns (PRON)
    """
    # Comparative adverbs (RBR)
    matcher = MatchersFactory.ambiguous_test_comparative_adverbs_matcher()

    # Actions
    for step in test.steps:
        action_matches = matcher(step.action)
        for match_id, start, end in action_matches:
            span = step.action[start:end]  # The matched span of tokens
            resultsWritter().write(
                [test.file, index, 'Ambiguous Test', 'comparative adverb', 'step', span, step.action])

    # Results
    for step in test.steps:
        # reactions = step.reactions
        # if len(step.reactions) == 1:
        #     reactions = [step.reactions]
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                span = reaction[start:end]  # The matched span of tokens
                resultsWritter().write(
                    [test.file, index, 'Ambiguous Test', 'comparative adverb', 'verification', span, reaction])

    # Adverbs of manner(RB)
    matcher = MatchersFactory.ambiguous_test_adverbs_of_manner_matcher()

    # Actions
    for step in test.steps:
        action_matches = matcher(step.action)
        for match_id, start, end in action_matches:
            span = step.action[start:end]
            if str(span[-1]).endswith(('ly', 'mente')):
                resultsWritter().write(
                    [test.file, index, 'Ambiguous Test', 'adverb of manner', 'step', span, step.action])

    # Results
    for step in test.steps:
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                span = reaction[start:end]
                if str(span[-1]).endswith(('ly', 'mente')):
                    resultsWritter().write(
                        [test.file, index, 'Ambiguous Test', 'adverb of manner', 'verification', span, reaction])

    # Adjectives
    matcher = MatchersFactory.ambiguous_test_adjectives_matcher()

    # Actions
    for step in test.steps:
        action_matches = matcher(step.action)
        for match_id, start, end in action_matches:
            span = step.action[start:end]
            resultsWritter().write([test.file, index, 'Ambiguous Test', 'adjective', 'step', span, step.action])

    # Results
    for step in test.steps:
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                span = reaction[start:end]
                resultsWritter().write(
                    [test.file, index, 'Ambiguous Test', 'adjective', 'verification', span, reaction])

    # Verb + indefinite determiner
    matcher = MatchersFactory.ambiguous_test_indefinite_determiners_matcher()

    # Actions
    for step in test.steps:
        action_matches = matcher(step.action)
        for match_id, start, end in action_matches:
            span = step.action[start:end]
            if "Definite=Def" not in str(span[-1].morph):  # spaCy recognizes definite determiners, which we don't want
                resultsWritter().write(
                    [test.file, index, 'Ambiguous Test', 'verb + indefinite determiner', 'step', span, step.action])

    # Results
    for step in test.steps:
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                span = reaction[start:end]
                if "Definite=Def" not in str(
                        span[-1].morph):  # spaCy recognizes definite determiners, which we don't want
                    resultsWritter().write(
                        [test.file, index, 'Ambiguous Test', 'verb + indefinite determiner', 'verification', span,
                         reaction])

    # Indefinite pronouns
    matcher = MatchersFactory.ambiguous_test_indefinite_pronouns_matcher()

    # Actions
    for step in test.steps:
        action_matches = matcher(step.action)
        for match_id, start, end in action_matches:
            span = step.action[start:end]
            if "PronType=Ind" in str(span[-1].morph):
                resultsWritter().write(
                    [test.file, index, 'Ambiguous Test', 'indefinite pronoun', 'step', span, step.action])

    # Results
    for step in test.steps:
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                span = reaction[start:end]
                if "PronType=Ind" in str(span[-1].morph):
                    resultsWritter().write(
                        [test.file, index, 'Ambiguous Test', 'indefinite pronoun', 'step', span, reaction])
