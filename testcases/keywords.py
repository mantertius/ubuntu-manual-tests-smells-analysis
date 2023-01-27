from data import expand_words

class Keywords:
    def __init__(self, language:str):
        self.language = language
        self.keywords = dict()
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
