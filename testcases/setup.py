'''
* The setup.py of the project.

The requirements.txt is created from it by using pip-tools with:

* pip-compile .
'''
from setuptools import setup, find_packages

setup(
    name='manual_test_smells',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['spacy',
                        'pandas',
                        'rich',
                        'scipy',
                        'lxml'
                        ]
)