from data import expand_words
import sys

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Keywords(metaclass=Singleton):
    def __init__(self, language:str=None):
        self.keywords = dict()
        if not language:
            language = 'english'
        if language == 'english':
            self.selector = self._english
        elif language == 'portuguese':
            self.selector = self._portuguese
        self.selector()

    def _english(self):
        verifications = ('check', 'verify', 'observe', 'recheck')
        # verifications = expand_words(verifications, k=5)
        verifications = ('verify', 'validate', 'observing', 'observe', 'checking', 'check', 'recheck', 'rechecked')
        self.keywords['verifications'] = verifications

    def _portuguese(self):
        verifications = ('checar', 'verificar', 'observar', 'rechecar', 're-rechecar')
        self.keywords['verifications'] = verifications

if __name__ == '__main__':
    k = Keywords('portuguese')
