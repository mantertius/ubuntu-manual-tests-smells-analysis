1) Unverified Steps: A step has no verification


2) Conditional Test: We count the number of conditional words for every test. We consider a word as conditional if it indicates a case
differentiation phrased in natural language (we used the words: if, whether, depending, when, in case). A test contains a smell if it contains at least one of those words. (Hauptman)

3) Eager Test: A test makes verifications on more than one object. (count the number of commands on the test)


4) Eager Step: A step makes more than one verification. (count the number of verifications on the test, if >1 then it's a smell)

5) Misplaced Pre-Condition: We count the number of "ensure"-like words for every test. We used the words: "make sure", "make certain","see to it","secure","guarantee","warrant",'certify','set the seal on', 'clinch', 'confirm', 'check','verify', 'corroborate', 'establish', 'sew up'.

6) Unspecified Parameter: We count the number of unspecific words for every test. The words used are: "all", "default", "any", "some".

7) Omission of Steps: When a step asks the tester for something he has not done.
8) Misplaced Step: We count the number of verbs on the verification section of the test. If there's more than one, than it's a smell.
9) Unspecified Wait: We count the "wait"-like words for every test. We consider these words: "wait", "halt", "rest", "holdup", "stay on hold".


10) Automatic Intervention: We search for execution of automatic step link, macro or script) in any section of the test.


11) Exception Handling: We count the number of question marks on every test.

12) Misplaced Result: We count the number of commands on the step section of the test. If there's more than one, it's already an ES and we must check if the extra command may be a verification, i.e. it can fit on the verification section.
13) Nested Test: We count the number of "Test" words on the step section. If there is more than zero, than there is a smell.
14) Test Clone: We look for similarities on the tests.
15) Magic Value: We check for a specific numerical value, that has no apparent meaning.
16) Random Data: We search for "random"-like words on the test. We used the words: "random", "any", "arbitrarily", "whatever", "whatsoever"
17) Calculating Expected Results On The Fly: ?
18) Optional Test: We count the word "optional" on every test. If there's any, than it's a smell.
19) Tacit Knowledge: When a step assumes something, but it has not commanded this early. (is this Omission of Step?)