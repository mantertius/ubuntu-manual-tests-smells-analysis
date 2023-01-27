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
        actions = ('check', 'verify', 'observe', 'recheck')
        actions = expand_words(actions, k=5)
        self.keywords['actions'] = actions

    def _portuguese(self):
        actions = ('checar', 'verificar', 'observar', 'rechecar', 're-rechecar')
        self.keywords['actions'] = actions

if __name__ == '__main__':
    k = Keywords('portuguese')
