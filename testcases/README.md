# Implementation Tracking 🕵🏻
#### 1. Unverified Steps - DONE ✅

#### 2. Automatic Intervention - is it possible? ❓
Manoel: check if there are script constructs throughout the test case, or if there are asserts. I don't know if it is possible and how can one detect these things.
#### 3. Exception Handling - DONE ✅

#### 4. Eager Test - DONE ✅

#### 5. Misplaced Pre-Condition ~~Pre-Condition As Step~~ - is it possible? ❓
Naelson: it's improbable that this can be detected using nlp - maybe using some kind of classification only on verbs and adverbs of the steps - only maybe.
#### 6. Misplaced Step ~~Expected Result as Step~~ - DONE ✅

#### 7. Misplaced Result - pending ➖
Naelson: Check for active pronouns in the steps. If there's any, than it's a misplaced result.
#### 8. Aimless Test - is it possible? ❓
Manoel: the header should contain information about the objective of the test. Can we check if there's a header?

#### 9. Conditional Test Logic - pending ➖
Naelson: branch detection may be a way.
#### 10. Unspecified Parameter - pending ➖
Naelson: this one may be hard, maybe looking at more examples may bring me more ideas.
#### 11. Undefined Wait - DONE ✅

#### 12. Nested Test - is it possible? ❓
Manoel: how can we detected if there is a test inside a test? If there's good documentation, we'll know by the name of the file or test the objective and them we can check if there's some kind of correlation between the

#### 13. Eager Step - DONE ✅

#### 14. Magic Value - is it possible? ❓
Manoel: what is the classification of a magic value? something that is used but there is no explanation to 

#### 15. Tacit Knowledge - is it possible? ❓
Manoel: one can check if there's repetition of this word throught the text. if it is repeated various times, we can safely say that the knowledge of the meaning of this word is rooted upon the tester. Even then, there may be some kind of new word that is only used once and does not comes with explanations. Maybe if we could see some kind of word set this would be easier.
#### 16. Random Data - is it possible? ❓
Manoel: use spacy's matcher to look for words that describe randomness? 