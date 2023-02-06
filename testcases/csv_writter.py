import csv

class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class resultsWritter(metaclass=SingletonMeta):

    csv_writer = ''

    def __init__(self):
        csv_header = ['Test name/file', 'Test Smell', 'Hint', 'Where', 'Term', 'Sentence']
        file = open('results.csv', 'w', encoding="UTF8", newline='')
        self.csv_writer = csv.writer(file)
        self.csv_writer.writerow(csv_header)

    def write(self, row: []):
        self.csv_writer.writerow(row)
