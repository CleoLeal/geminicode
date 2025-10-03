import pandas as pd
import os

def carregar_dataset():
    # caminho correto considerando que assets está fora de app
    path = os.path.join(os.path.dirname(__file__), "dataset_velocidade_v2.xlsx")
    
    # converte para caminho absoluto
    path = os.path.abspath(path)
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    
    df = pd.read_excel(path)
    return df
