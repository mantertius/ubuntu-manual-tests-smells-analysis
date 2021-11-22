# Ubuntu Manual Test Smell Analysis
This repository contains the manual testcases utilized by the quality team for testing ubuntu (and its flavors) packages and images, as well as manual tests for hardware compatibility. 

Also, this is a fork of [Ubuntu Manual Tests](https://launchpad.net/ubuntu-manual-tests) that has been analyzed in search of test smells. These smells are based on Hauptmann et al. and on the [Open Test Smells Catalog](https://eas5.github.io/index.html).

## Manual Test Smells Found
These are the ones that we have found so far:
1. UNVERIFIED STEPS: a step that does not comes with a expected result section;
2. NON-MANUAL TEST: a test suite that contains any kind of automatic verifications, i.e. asserts, scripts, etc.;
3. QUESTIONING STEPS: a step that ends with a question mark, asking something for the tester;
4. LONG EXPECTED RESULTS: a test suite that contains too many items in the ER session for a single step;
5. PRE-STEP AS STEP: a step that is not a step, but a preparation for the test itself. Generally starts with "Ensure";
6. EXPECTED RESULTS AS STEP: a step that is not a step, but is a expected result;
7. UNSPECIFIED WAITING TIME: a step that doenst specifies the time that the tester must wait for the expected result to happen. Generally starts with "Wait";
8. AIMLESS TEST: a test without an clear objective written before the preparation for the test;
9. EAGER TEST: a test where the a part of the ER session could be tested by another step, i.e. there's two ERs to only one step
10. CONDITIONAL TEST LOGIC: a step that changes the flow of testing based on some conditional. If there is more than one way to execute the test, the different ways should be different tests. Generally stars with "If";
11. UNSPECIFIED PARAMETER: occurs when a test or a step comes without a specified parameter, i.e. the tester doesnt knows what to test. May contain "all".




