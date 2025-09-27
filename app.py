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
from datetime import datetime
import dash_daq as daq
from collections import deque

# --------------------------
# 1️⃣ Modelo de Treinamento com margem
# --------------------------
df = pd.read_excel("./dataset/dataset_velocidade_v2.xlsx")

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

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <!-- Google Fonts: Poppins -->
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Armazenamento em tempo real
dados_reais = pd.DataFrame(columns=['timestamp', 'velocidade', 'status', 'anomalia'])

estatisticas = {
    "total_anomalias": 0,
    "tempo_normal": 0,
    "tempo_anomalo": 0,
    "velocidades": deque(maxlen=1000)
}

# Layout
app.layout = html.Div(
    style={
        "backgroundColor": "#ffffff",
        "color": "#000000",
        "font-family": "Poppins, Exo",
        "padding": "20px"
    },
    children=[
        html.H1("Monitoramento do Atuador", style={"textAlign": "center", "color": "#A020F0"}),

        dcc.Interval(
            id="intervalo",
            interval=1000,  # 1 segundo
            n_intervals=0
        ),

        html.Div([
            html.Label("Filtrar últimos minutos:", style={"marginRight": "10px"}),
            dcc.Dropdown(
                id="filtro-tempo",
                options=[
                    {"label": "1 min", "value": 1},
                    {"label": "5 min", "value": 5},
                    {"label": "10 min", "value": 10},
                    {"label": "Todos", "value": "all"}
                ],
                value="all",
                clearable=False,
                style={"width": "200px", "color": "#000"}
            ),
            daq.ToggleSwitch(
                id="toggle-pausa",
                label="Pausar Atualização",
                labelPosition="top",
                value=False,
                style={"marginLeft": "20px"}
            )
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "30px"}),

        # ---------- Linha 1: Gráfico de Linha + Indicadores + Pizza ----------
        html.Div([
            # Gráfico de linha (lado esquerdo)
            dcc.Graph(id="grafico-linha", style={
                "flex": "3",
                "marginRight": "10px",
                "backgroundColor": "#1A1A1A",
                "borderRadius": "15px",
                "padding": "10px",
                "height": "100%"   # 👈 ocupa a altura da linha inteira
            }),

            # Coluna da direita (cards + gráfico de pizza)
            html.Div([
                # Cards lado a lado
                html.Div(id="cards-estatisticas", style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "marginBottom": "10px",
                    "gap": "10px",
                    "color": "#F5F5F5"  
                }),

                # Gráfico de pizza
                dcc.Graph(id="grafico-pizza", style={
                    "backgroundColor": "#1A1A1A",
                    "borderRadius": "15px",
                    "padding": "10px",
                    "flex": "1"  # garante que o pizza preencha
                })
            ], style={
                "flex": "1",
                "display": "flex",
                "flexDirection": "column",
                "height": "100%"   # 👈 mesma altura da linha
            })
        ], style={
            "display": "flex",
            "marginBottom": "15px",
            "alignItems": "stretch"  # 👈 força as colunas a terem mesma altura
        }),

        # ---------- Linha 2: Histograma ----------
        html.Div([
            dcc.Graph(id="grafico-histograma", style={
                "backgroundColor": "#1A1A1A",
                "borderRadius": "15px",
                "padding": "10px",
                "width": "100%"
            })
        ])
    ]
)



# --------------------------
# 3️⃣ Atualização em tempo real
# --------------------------
@app.callback(
    [Output("grafico-linha", "figure"),
     Output("grafico-pizza", "figure"),
     Output("grafico-histograma", "figure"),
     Output("cards-estatisticas", "children")],
    [Input("intervalo", "n_intervals"),
     Input("filtro-tempo", "value"),
     Input("toggle-pausa", "value")]
)
def atualizar_dashboard(n, filtro_minutos, pausado):
    global dados_reais, estatisticas
    
    if not pausado:
        # -------- Gerar novo valor simulado --------
        prob_anomalia = 0.05
        if random.random() < prob_anomalia:
            # Gera fora da faixa
            if random.random() < 0.5:
                velocidade = round(random.uniform(0.06, limite_inferior - 0.001), 4)
            else:
                velocidade = round(random.uniform(limite_superior + 0.001, 0.12), 4)
        else:
            # Gera em torno do ideal com ruído + seno
            amplitude = 0.002
            ruido_max = 0.001
            if len(dados_reais) == 0:
                velocidade = ideal
            else:
                velocidade = round(
                    ideal + amplitude * math.sin(n * 0.1) + random.uniform(-ruido_max, ruido_max), 4
                )
                velocidade = max(limite_inferior, min(limite_superior, velocidade))
        
        movimento = random.choice(['avanco', 'recuo'])
        movimento_num = le.transform([movimento])[0]
        novo_dado = pd.DataFrame({'velocidade':[velocidade], 'movimento_num':[movimento_num]})
        
        # -------- Classificação com modelo treinado --------
        pred = model.predict(novo_dado)
        anomalia = pred[0] == 0   # 0 = anomalia
        status = "Anomalia" if anomalia else "Normal"
        
        # -------- Adicionar ao histórico --------
        timestamp = datetime.now()
        novo_registro = pd.DataFrame({
            'timestamp': [timestamp],
            'velocidade': [velocidade],
            'status': [status],
            'anomalia': [anomalia]
        })
        dados_reais = pd.concat([dados_reais, novo_registro], ignore_index=True)
        
        # Atualizar estatísticas
        if anomalia:
            estatisticas['total_anomalias'] += 1
            estatisticas['tempo_anomalo'] += 1
        else:
            estatisticas['tempo_normal'] += 1
        
        estatisticas['velocidades'].append(velocidade)

    # Filtrar dados
    if filtro_minutos != "all":
        limite_tempo = datetime.now() - pd.Timedelta(minutes=filtro_minutos)
        dados_filtrados = dados_reais[dados_reais['timestamp'] >= limite_tempo]
    else:
        dados_filtrados = dados_reais

    # -------- Gráfico de Linha --------
    fig_linha = go.Figure()
    if not dados_filtrados.empty:
        # Pegar apenas as últimas 35 amostras
        dados_plot = dados_filtrados.tail(35)

        fig_linha.add_trace(go.Scatter(
            x=dados_plot['timestamp'],  
            y=dados_plot['velocidade'],
            mode="lines+markers",
            line=dict(color="#A020F0"),
            marker=dict(color=dados_plot['anomalia'].map({True: "red", False: "green"})),
            name="Velocidade",
            line_shape="spline"
        ))

    # 🔥 Definir altura fixa do gráfico
    fig_linha.update_layout(
        template="plotly_dark",
        title="Velocidade em Tempo Real (Últimas 35 amostras)",
        xaxis_title="Tempo",
        yaxis_title="Velocidade",
        height=628  # 👈 ajusta a altura do gráfico de linha
    )

    # -------- Gráfico de Pizza --------
    fig_pizza = go.Figure(data=[go.Pie(
        labels=["Normal", "Anomalia"],
        values=[estatisticas['tempo_normal'], estatisticas['tempo_anomalo']],
        hole=0.5,
        marker=dict(colors=["#6A0DAD", "#FF4500"])
    )])
    fig_pizza.update_layout(
    template="plotly_dark",
    title="Distribuição de Status",
    legend=dict(
        orientation="v",   # legenda na horizontal
        yanchor="bottom",
        y=-0.2,            # joga a legenda para baixo do gráfico
        xanchor="center",
        x=0.5
    )
)

    # -------- Histograma --------
    fig_hist = go.Figure()
    if estatisticas['velocidades']:
        fig_hist.add_trace(go.Histogram(
            x=list(estatisticas['velocidades']),
            nbinsx=20,
            marker_color="#A020F0"
        ))
    fig_hist.update_layout(template="plotly_dark", title="Distribuição de Velocidades", width=1470)

    # -------- Cards --------
    cards = [
        html.Div([
            html.H4("Total Anomalias", style={"textAlign": "center"}),
            html.P(estatisticas['total_anomalias'], style={"fontSize": "24px", "color": "#FF4500", "textAlign": "center"})
        ], style={
            "padding": "20px",              # mais espaço interno
            "backgroundColor": "#1A1A1A",
            "borderRadius": "10px",
            "flex": "1",                    # ocupa largura proporcional
            "textAlign": "center"
        }),

        html.Div([
            html.H4("Tempo Normal", style={"textAlign": "center"}),
            html.P(estatisticas['tempo_normal'], style={"fontSize": "24px", "color": "#00FF7F", "textAlign": "center"})
        ], style={
            "padding": "20px",
            "backgroundColor": "#1A1A1A",
            "borderRadius": "10px",
            "flex": "1",
            "textAlign": "center"
        }),
    ]

    return fig_linha, fig_pizza, fig_hist, cards

# --------------------------
# 4️⃣ Executar app
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)
