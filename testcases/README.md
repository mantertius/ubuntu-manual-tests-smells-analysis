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