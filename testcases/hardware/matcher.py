import pandas as pd

df = pd.read_csv('files.csv')

FILE_COL = 'NUMERO E NOME DO ARQUIVO'
SMELL_COL = 'QUAL SMELL?'
df[FILE_COL] = df[FILE_COL].apply(lambda x: x.split(' - ')[-1])
df[SMELL_COL] = df[SMELL_COL].fillna('')
df[SMELL_COL] = df[SMELL_COL].apply(lambda x: x.replace(' ', '').split(','))
df = df[[FILE_COL,SMELL_COL]]