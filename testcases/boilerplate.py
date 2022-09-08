from rich import print
import spacy
from spacy.matcher import Matcher
nlp = spacy.load('en_core_web_sm')

text = 'In the second part of the study, we leverage the previously detected clusters of test steps to identify similar test cases. We compared three different techniques and related variations to compute a similarity score (using the simple overlap, Jaccard, and cosine metrics) to measure the similarity of test cases based on the test step clusters that they have in common. In particular, we address the following research question for this part of the study: RQ2: How can we leverage clusters of test steps to identify similar test cases? Given the difficulty of identifying similar test cases, which areusually composed of several steps, we use clusters of similar teststeps to identify similar test cases. We found that test step clusterscan be used to identify test case similarity with a high performance(an F-score of 83.47%).'
text2 = 'Closed. This question needs details or clarity. It is not currently accepting answers. Want to improve this question? Add details and clarify the problem by editing this post. Closed 8 years ago. How to wait for 2 minutes for method to complete, but if it does not complete then Exit and continue? I want to wait for 2 minutes for method to complete, but if it does not complete in 2 minutes then Exit execution and continue ahead. Wait for a hundred years, wait for a day, wait until tomorrow, wait for the day, wait for the window to popup, wait for three hours'
text3 = """dt>Press continue</dt>
        <dd>The 'Welcome to FAMILY ' slide is displayed</dd>
        <dd>The slideshow is entirely in your language</dd> 
<!-- Smell: Unspecified Waiting Time -->
    <dt>Wait for the installer to finish</dt>
        <dd>An 'Installation Complete' dialog appears</dd>
    <dt>Click the Restart now button</dt>'
"""
doc = nlp(text3)
WAIT_LIKE_VERBS = ["wait",
"time interval",
"down",
"downtime",
"halt",
"hold",
"interim",
"rest",
"stay",
"holdup",
"on hold",
"time wasted",'Wait']

matcher = Matcher(nlp.vocab)
pattern = [{'ORTH': {"IN" : WAIT_LIKE_VERBS}}] #'POS': 'ADP', 'LIKE_NUM': True}]

pattern2 = [{'ORTH': {"IN" : WAIT_LIKE_VERBS}},{'POS' : 'ADP', 'OP' : '+'} , {'LIKE_NUM' : False}]

def on_match(matcher, doc, id, matches):
    for match_id, start, end in matches:
        span = doc[start:end]
        string_id = nlp.vocab.strings[match_id]
        print(f'[{string_id}]:{span.text}')

#matcher.add("FOUND_WAIT",[pattern],on_match=on_match)
#matcher.add("TEST_PATTERNS", patterns, on_match=on_match)
#matches = matcher(doc)
#num_of_waits_found = len(matches)
matcher.add("NOT_NUM",[pattern2],on_match=on_match)
matches = matcher(doc)
result = len(matches)
#num_of_not_num = len(matches) - num_of_waits_found
#result = num_of_not_num - num_of_waits_found

#print(matches)
breakpoint()
#print(f'{matches}')

#print(f'{nlp(text)}')