#importações
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

#função para treinar o modelo
def treinar_modelo(df, limite_inferior, limite_superior):
    # preparação dos dados
    df['flag_margem'] = df['velocidade'].between(limite_inferior, limite_superior).astype(int)
    # treinamento do modelo
    le = LabelEncoder()
    df['movimento_num'] = le.fit_transform(df['movimento'])
    X = df[['velocidade', 'movimento_num']]
    y = df['flag_margem']
    # ivisão dos dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    # treinamento do modelo RandomForest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model, le
