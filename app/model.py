import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier


def treinar_modelo(df, ideal=0.08, margem=0.05):
    limite_inferior = ideal * (1 - margem)
    limite_superior = ideal * (1 + margem)

    # Criar flag
    df['flag_margem'] = df['velocidade'].between(limite_inferior, limite_superior).astype(int)

    # Label Encoder
    le = LabelEncoder()
    df['movimento_num'] = le.fit_transform(df['movimento'])

    # Features e target
    X = df[['velocidade', 'movimento_num']]
    y = df['flag_margem']

    # Treino/teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Treinar modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model, le

