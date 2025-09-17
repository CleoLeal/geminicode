import pandas as pd
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go  # Usamos go para múltiplas linhas

# --------------------------
# 1️⃣ Modelo Random Forest (igual antes)
# --------------------------
df = pd.read_excel("C:/Users/Cleo Leal/Documents/GitHub/geminicode/dataset/dataset_velocidade.xlsx")

le_mov = LabelEncoder()
df['movimento'] = le_mov.fit_transform(df['movimento'])

le_flag = LabelEncoder()
df['flag_anomalia'] = le_flag.fit_transform(df['flag_anomalia'])

X = df[['movimento','tempo_movimento','velocidade']]
y = df['flag_anomalia']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

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
    
    # Gerar valor aleatório do teste
    velocidade = round(random.uniform(0.067, 0.116), 4)
    
    # Classificar
    pred = clf.predict(pd.DataFrame({'movimento':[0],'tempo_movimento':[0.08],'velocidade':[velocidade]}))
    status = "Anomalia" if pred[0]==1 else "Normal"
    
    # Adicionar ao histórico
    dados_reais = pd.concat([dados_reais, pd.DataFrame({'velocidade':[velocidade],'status':[status]})], ignore_index=True)
    
    # Criar gráfico
    fig = go.Figure()
    
    # Linha fixa de referência
    fig.add_trace(go.Scatter(
        y=[0.08]*len(dados_reais),
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
    
    fig.update_layout(title="Velocidade do Atuador - Real x Ideal",
                      xaxis_title="Tempo (passos)",
                      yaxis_title="Velocidade",
                      yaxis=dict(range=[0, 0.12]))
    
    return fig

# --------------------------
# 4️⃣ Rodar app
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)
