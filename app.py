import pandas as pd
import random
import math
from sklearn.model_selection import train_test_split
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import plotly.graph_objects as go

# --------------------------
# 1️⃣ Modelo de Treinamento (Random Forest)
# --------------------------
df = pd.read_excel("dataset/dataset_velocidade_v2.xlsx")

# Codificar movimento
le = LabelEncoder()
df['movimento_num'] = le.fit_transform(df['movimento'])

# Definir flag considerando margem de erro de 5%
ideal = 0.08
margem = 0.05
limite_inferior = ideal * (1 - margem)
limite_superior = ideal * (1 + margem)

df['flag_margem'] = df['velocidade'].apply(
    lambda x: 1 if limite_inferior <= x <= limite_superior else 0
)

# Features e target
X = df[['velocidade', 'movimento_num']]
y = df['flag_margem']  # 1 = normal, 0 = anomalia

# Dividir treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Treinar Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

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
    prob_anomalia = 0.05
    
    # Gerar velocidade
    if random.random() < prob_anomalia:
        if random.random() < 0.5:
            velocidade = round(random.uniform(0.06, limite_inferior - 0.001), 4)
        else:
            velocidade = round(random.uniform(limite_superior + 0.001, 0.12), 4)
    else:
        amplitude = 0.002
        ruido_max = 0.001
        if len(dados_reais) == 0:
            velocidade = ideal
        else:
            ultimo = dados_reais['velocidade'].iloc[-1]
            velocidade = round(ideal + amplitude * math.sin(n*0.1) + random.uniform(-ruido_max, ruido_max), 4)
            velocidade = max(limite_inferior, min(limite_superior, velocidade))
    
    # Gerar movimento aleatório
    movimento = random.choice(['avanco', 'recuo'])
    
    # Preparar dado para predição
    movimento_num = le.transform([movimento])[0]
    novo_dado = pd.DataFrame({'velocidade':[velocidade], 'movimento_num':[movimento_num]})
    
    # Predição Random Forest
    pred = model.predict(novo_dado)
    status = "Normal" if pred[0]==1 else "Anomalia"
    
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
