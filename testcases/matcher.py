import pandas as pd
from pathlib import Path
DIR_COL = 'DIRETÓRIO'
FILE_COL = 'NUMERO E NOME DO ARQUIVO'
SMELL_COL = 'QUAL SMELL?'

def smells_loader_closure():
    df = pd.read_csv('files.csv')
    #df[FILE_COL] = df[FILE_COL].apply(lambda x: x.split(' - ')[-1])
    df[SMELL_COL] = df[SMELL_COL].fillna('')
    df[SMELL_COL] = df[SMELL_COL].apply(lambda x: x.replace(' ', '').split(','))
    df[FILE_COL] = df[DIR_COL]+df[FILE_COL]
    df = df[[FILE_COL, SMELL_COL]]
    df = df.loc[df[FILE_COL].apply(lambda x: Path(x).exists())]
    df[FILE_COL] = df[FILE_COL].apply(lambda x: Path(x))

    def smells_loader(smell:str) -> pd.DataFrame:
        return df.loc[df[SMELL_COL].apply(lambda x: smell in x)].reset_index(drop=True)

    return smells_loader

if __name__ == '__main__':
    smells_loader = smells_loader_closure()
    df = smells_loader('US')