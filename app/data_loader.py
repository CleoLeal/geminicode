#importações
import pandas as pd
#função para carregar o dataset
def carregar_dataset(path="../assets/dataset_velocidade_v2.xlsx"):
    df = pd.read_excel(path)
    df['movimento'] = df['movimento'].astype(str)
    return df

print("Carregado com sucesso")
