import pandas as pd
import random
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
cat_features = ['movimento']        # movimento como categórico
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
# 3️⃣ Callback para gráfico com linha fixa + resultados
# --------------------------
@app.callback(
    Output('grafico_velocidade', 'figure'),
    Input('intervalo-atualizacao', 'n_intervals')
)
def atualizar_grafico(n):
    global dados_reais
    
    # Gerar valores aleatórios
    velocidade = round(random.uniform(0.067, 0.116), 4)   # float
    tempo = round(random.uniform(1.0, 1.5), 3)           # float
    movimento = str(random.choice([0, 1]))               # string, consistente com o dataset
    
    # Montar DataFrame para predição
    novo_dado = pd.DataFrame({
        'movimento': [movimento],
        'tempo': [tempo],
        'velocidade': [velocidade]
    })
    
    # Predição
    pred = pipeline.predict(novo_dado)
    status = "Anomalia" if pred[0]==1 else "Normal"
    
    # Adicionar ao histórico
    dados_reais = pd.concat(
        [dados_reais, pd.DataFrame({'velocidade':[velocidade], 'status':[status]})],
        ignore_index=True
    )
    
    # Criar gráfico
    fig = go.Figure()
    
    # Linha fixa de referência
    fig.add_trace(go.Scatter(
        y=[ideal]*len(dados_reais),
        mode='lines',
        name='Velocidade Ideal',
        line=dict(color='green', dash='dash')
    ))
    
    # Linha de resultados do teste
    fig.add_trace(go.Scatter(
        y=dados_reais['velocidade'],
        mode='lines+markers',
        name='Velocidade Real',
        line=dict(color='blue')
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
