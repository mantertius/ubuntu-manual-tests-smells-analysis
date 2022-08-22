# Installing
To run the program, you must install some packages. They are listed on requirements.txt, but for some unknown reason, it does not download everything that it should be. 

Because of this, go to your venv (you should have one) and download these:

`pip install spacy && pip install pandas && pip install rich`

Then, install the requirements.

`pip install -r requirements.txt`

After downloading everything, you must download spacy's model.

`python -m spacy download en_core_web_sm`

After this, you are done.

# Running
To run the program, simply call it using the python runner and follow the instructions:

`python matcher.py`

For now, it only runs in UNIX.
# Implementation Tracking 🕵🏻
#### 1. Unverified Steps - DONE ✅

#### 2. Automatic Intervention - is it possible? ❓
Manoel: check if there are script constructs throughout the test case, or if there are asserts. I don't know if it is possible and how can one detect these things.
#### 3. Exception Handling - DONE ✅

#### 4. Eager Test - DONE ✅

#### 5. Misplaced Pre-Condition ~~Pre-Condition As Step~~ - is it possible? ❓
Naelson: it's improbable that this can be detected using nlp - maybe using some kind of classification only on verbs and adverbs of the steps - only maybe.
#### 6. Misplaced Step ~~Expected Result as Step~~ - DONE ✅

#### 7. Misplaced Result ~~Step as Expected Result~~ - pending ➖
Naelson: Check for active pronouns in the steps. If there's any, than it's a misplaced result.
#### 8. Aimless Test - is it possible? ❓
Manoel: the header should contain information about the objective of the test. Can we check if there's a header?

#### 9. Conditional Test Logic - DONE ✅
Naelson: branch detection may be a way.

Manoel: Sounds like what you want to do relies on discourse parsing. It basically detects relations between sentences (or phrases) and classifies them according to sense, and one of these senses can be condition (others are, for example, comparison, contrast, expansion, etc.). There are a few discourse parsers around (try googling English discourse parser in combination with PDTB or RST), but this is a quite challenging sub-field of NLP with typically not too high f-scores (due to low inter-annotator agreement and only limited training data available, among other things). As far as I know, anything in this direction is not included in NLTK (or corenlp of opennlp for that matter). A good start might be this one (https://wing.comp.nus.edu.sg/~linzihen/parser/), but it's not in python (but in Java or Ruby). https://stackoverflow.com/a/45617563/8519227

Manoel: I've thought about it and maybe we could just search for "if"s and then go for it. That's what I did.
#### 10. Unspecified Parameter - pending ➖
Naelson: this one may be hard, maybe looking at more examples may bring me more ideas.
#### 11. Undefined Wait - DONE ✅

#### 12. Nested Test - is it possible? ❓
Manoel: how can we detected if there is a test inside a test? If there's good documentation, we'll know by the name of the file or test the objective and them we can check if there's some kind of correlation between the

#### 13. Eager Step - pending ➖
Manoel: similar to eager test

#### 14. Magic Value - is it possible? ❓
Manoel: what is the classification of a magic value? something that is used but there is no explanation to 

#### 15. Tacit Knowledge - is it possible? ❓
Manoel: one can check if there's repetition of this word throught the text. if it is repeated various times, we can safely say that the knowledge of the meaning of this word is rooted upon the tester. Even then, there may be some kind of new word that is only used once and does not comes with explanations. Maybe if we could see some kind of word set this would be easier.
#### 16. Random Data - is it possible? ❓
Manoel: use spacy's matcher to look for words that describe randomness? 

#### 17. Optional Test - DONE ✅

# Implementation Rules
1) Unverified Steps: A step has no verification

2) Conditional Test: We count the number of conditional words for every test. We consider a word as conditional if it indicates a case
differentiation phrased in natural language (we used the words: if, whether, depending, when, in case). A test contains a smell if it contains at least one of those words. (Hauptmann) 

3) Eager Test: A test makes verifications on more than one object. (count the number of commands on the test)

4) Eager Step: A step makes more than one verification. (count the number of verifications on the test, if >1 then it's a smell)

5) Misplaced Pre-Condition: We count the number of "ensure"-like words for every test. We used the words: "make sure", "make certain","see to it","secure","guarantee","warrant",'certify','set the seal on', 'clinch', 'confirm', 'check','verify', 'corroborate', 'establish', 'sew up'. [word embedding]

* facil de fazer 6) Unspecified Parameter: We count the number of unspecific words for every test. The words used are: "all", "default", "any", "some". [Matcher de dependencia]

-- on hold 7) Omission of Steps: When a step asks the tester for something he has not done.

8) Misplaced Step: Tem um passo no lugar de um resultado esperado. Verbo imperativo no resultado

9) Unspecified Wait: We count the "wait"-like words for every test. We consider these words: "wait", "halt", "rest", "holdup", "stay on hold". [word embedding]

-- on hold 10) Automatic Intervention: We search for execution of automatic step (link, macro or script) in any section of the test.

11) Exception Handling: We count the number of question marks on every test. "?" [trocar nome]

12) Misplaced Result: Theres a verification instead of a step. 

-- on hold 13) Nested Test: We count the number of "Test" words on the step section. If there is more than zero, than there is a smell.

14) Test Clone: Following the definition from [1], we consider a test clone as a substring of a test with at least 30 words appearing at least twice in a test suite. To find clones which differ slightly (e. g., because of inconsistent typo fixes), clones are allowed to have minor variations such that the difference (the gap) accounts for less than 10% of the length of the clone. A test contains a smell if it contains at least one clone. (Hauptmann) [cosine distance is a way to solve this]

-- on hold may give many false positives 15) Magic Value: We check for a specific value, that has no apparent meaning. 

16) Random Data: We search for "random"-like words on the test. We used the words: "random", "any", "arbitrarily", "whatever", "whatsoever" [word embedding]

-- impossible to detect 17) Calculating Expected Results On The Fly: ?

-- on hold 18) Optional Test: We count the word "optional" on every test. If there's any, than it's a smell. [word similarity]

-- hard to implement 19) Tacit Knowledge: When a step assumes something, but it has not commanded this early. (is this Omission of Step?)
-- SAME AS 19 7) Omission of Steps: When a step asks the tester for something he has not done.
