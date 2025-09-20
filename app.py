import pandas as pd
import random
import math
from sklearn.model_selection import train_test_split
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

# --------------------------
# 1️⃣ Modelo de Treinamento
# --------------------------
df = pd.read_excel("dataset/dataset_velocidade_v2.xlsx")

# Parâmetros da regra
ideal = 0.08
margem = 0.05
limite_inferior = ideal * (1 - margem)
limite_superior = ideal * (1 + margem)

# Criar target: 0 = normal, 1 = anomalia
df['target'] = ((df['velocidade'] < limite_inferior) | (df['velocidade'] > limite_superior)).astype(int)

# Features e target
X = df[['movimento', 'tempo', 'velocidade']]
y = df['target']

# Colunas categóricas e numéricas
cat_features = ['movimento']
num_features = ['tempo', 'velocidade']

# Pré-processamento
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
    ]
)

# Pipeline com Regressão Logística
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(random_state=42, max_iter=1000))
])

# Dividir dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo
pipeline.fit(X_train, y_train)

# --------------------------
# 2️⃣ Dashboard
# --------------------------
app = Dash(__name__)
dados_reais = pd.DataFrame(columns=['velocidade','status'])

app.layout = html.Div([
    html.H1("Sistema Pneumático - Monitoramento em Tempo Real"),
    
    dcc.Graph(id='grafico_velocidade'),
    dcc.Interval(id='intervalo-atualizacao', interval=1000, n_intervals=0)
])

# --------------------------
# 3️⃣ Callback para gráfico com linha fixa + resultados coloridos
# --------------------------
@app.callback(
    Output('grafico_velocidade', 'figure'),
    Input('intervalo-atualizacao', 'n_intervals')
)
def atualizar_grafico(n):
    global dados_reais
    
    # Probabilidade de gerar anomalia
    prob_anomalia = 0.05  # 10% das vezes
    
    # Se gerar anomalia, escolhe um valor fora do limite
    if random.random() < prob_anomalia:
        # 50% abaixo, 50% acima do limite
        if random.random() < 0.5:
            velocidade = round(random.uniform(0.06, limite_inferior - 0.001), 4)
        else:
            velocidade = round(random.uniform(limite_superior + 0.001, 0.12), 4)
    else:
        # Valor normal próximo de 0.08 com pequenas variações
        amplitude = 0.002
        ruido_max = 0.001
        if len(dados_reais) == 0:
            velocidade = ideal
        else:
            ultimo = dados_reais['velocidade'].iloc[-1]
            velocidade = round(ideal + amplitude * math.sin(n*0.1) + random.uniform(-ruido_max, ruido_max), 4)
            velocidade = max(limite_inferior, min(limite_superior, velocidade))
    
    # Dados de predição
    tempo = round(random.uniform(1.0, 1.5), 3)
    movimento = str(random.choice([0, 1]))
    
    novo_dado = pd.DataFrame({
        'movimento': [movimento],
        'tempo': [tempo],
        'velocidade': [velocidade]
    })
    
    pred = pipeline.predict(novo_dado)
    status = "Anomalia" if pred[0]==1 else "Normal"
    
    # Adicionar ao histórico
    dados_reais = pd.concat(
        [dados_reais, pd.DataFrame({'velocidade':[velocidade], 'status':[status]})],
        ignore_index=True
    )
    
    # Criar gráfico
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=[ideal]*len(dados_reais),
        mode='lines',
        name='Velocidade Ideal',
        line=dict(color='green', dash='dash')
    ))
    
    # Separar por status
    normais = dados_reais[dados_reais['status']=="Normal"]
    anomalias = dados_reais[dados_reais['status']=="Anomalia"]
    
    if len(normais) > 0:
        fig.add_trace(go.Scatter(
            y=normais['velocidade'],
            mode='lines+markers',
            name='Normal',
            line=dict(color='blue'),
            marker=dict(color='blue')
        ))
    
    if len(anomalias) > 0:
        fig.add_trace(go.Scatter(
            y=anomalias['velocidade'],
            mode='lines+markers',
            name='Anomalia',
            line=dict(color='red'),
            marker=dict(color='red')
        ))
    
    fig.update_layout(
        title="Velocidade do Atuador - Real x Ideal",
        xaxis_title="Tempo (passos)",
        yaxis_title="Velocidade",
        yaxis=dict(range=[0, 0.12])
    )
    
    return fig

# --------------------------
# 4️⃣ Rodar app
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)