import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import streamlit.components.v1 as components
import math
import base64

# --------------------------
# Configuração inicial
# --------------------------
st.set_page_config(page_title="Dashboard de Monitoramento", layout="wide")

# Dataset base
df = pd.read_excel("./dataset/dataset_velocidade_v2.xlsx")
df['movimento'] = df['movimento'].astype(str)

# Parâmetros fixos
ideal = 0.08
margem = 0.05
limite_inferior = ideal * (1 - margem)
limite_superior = ideal * (1 + margem)

# Criar flag (1 = Normal, 0 = Anômalo)
df['flag_margem'] = df['velocidade'].between(limite_inferior, limite_superior).astype(int)

# Treinar modelo
le = LabelEncoder()
df['movimento_num'] = le.fit_transform(df['movimento'])
X = df[['velocidade', 'movimento_num']]
y = df['flag_margem']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Sessão
if "dados_reais" not in st.session_state:
    st.session_state.dados_reais = pd.DataFrame(columns=["timestamp", "velocidade", "status"])
if "rodando" not in st.session_state:
    st.session_state.rodando = False
if "aba_ativa" not in st.session_state:
    st.session_state.aba_ativa = "tempo_real"

# --------------------------
# Funções auxiliares
# --------------------------
def gerar_dado(i):
    prob_anomalia = 0.1
    if random.random() < prob_anomalia:
        if random.random() < 0.5:
            velocidade = round(random.uniform(0.06, limite_inferior - 0.001), 4)
        else:
            velocidade = round(random.uniform(limite_superior + 0.001, 0.12), 4)
    else:
        amplitude = 0.002
        ruido_max = 0.001
        if len(st.session_state.dados_reais) == 0:
            velocidade = ideal
        else:
            velocidade = round(
                ideal + amplitude * math.sin(i * 0.1) + random.uniform(-ruido_max, ruido_max), 4
            )
            velocidade = max(limite_inferior, min(limite_superior, velocidade))

    movimento = random.choice(list(df['movimento'].unique()))
    movimento_num = le.transform([movimento])[0]
    pred = model.predict([[velocidade, movimento_num]])[0]
    status = "Normal" if pred == 1 else "Anômalo"

    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "velocidade": velocidade,
        "status": status
    }

# --------------------------
# Abas
# --------------------------
tab1, tab2, tab3 = st.tabs(["📈 Tempo Real", "📊 Estatísticas", "📄 Sobre"])

# --------------------------
# 📈 Aba 1 — Tempo Real
# --------------------------
with tab1:
    st.header("Monitoramento em Tempo Real")

    col1, col2, col3 = st.columns([1, 1, 1])
    iniciar = col1.button("▶️ Iniciar Simulação")
    parar = col2.button("⏹️ Parar Simulação")
    resetar = col3.button("♻️ Resetar Histórico")

    if iniciar:
        st.session_state.rodando = True
        st.session_state.aba_ativa = "tempo_real"

    if parar:
        st.session_state.rodando = False
        st.session_state.aba_ativa = "estatisticas"

    if resetar:
        st.session_state.dados_reais = pd.DataFrame(columns=["timestamp", "velocidade", "status"])

    placeholder = st.empty()

    if st.session_state.rodando:
        for i in range(1000000):
            if not st.session_state.rodando:
                break

            novo = gerar_dado(i)
            st.session_state.dados_reais = pd.concat(
                [st.session_state.dados_reais, pd.DataFrame([novo])],
                ignore_index=True
            )

            dados_plot = st.session_state.dados_reais.tail(30)

            fig = go.Figure()

            # Linha roxa arredondada
            fig.add_trace(go.Scatter(
                x=dados_plot["timestamp"],
                y=dados_plot["velocidade"],
                mode="lines",
                line=dict(shape="spline", smoothing=1.3, color="purple", width=3),
                showlegend=False
            ))

            # Bolinhas Normal (azul)
            fig.add_trace(go.Scatter(
                x=dados_plot[dados_plot["status"] == "Normal"]["timestamp"],
                y=dados_plot[dados_plot["status"] == "Normal"]["velocidade"],
                mode="markers",
                marker=dict(color="#1E90FF", size=10),
                name="Normal"
            ))

            # Bolinhas Anômalo (turquesa)
            fig.add_trace(go.Scatter(
                x=dados_plot[dados_plot["status"] == "Anômalo"]["timestamp"],
                y=dados_plot[dados_plot["status"] == "Anômalo"]["velocidade"],
                mode="markers",
                marker=dict(color="#00CED1", size=10),
                name="Anômalo"
            ))

            # Linhas de referência
            fig.add_hline(y=limite_inferior, line=dict(color="gray", dash="dash"))
            fig.add_hline(y=ideal, line=dict(color="black", dash="dot"))
            fig.add_hline(y=limite_superior, line=dict(color="gray", dash="dash"))

            fig.update_layout(
                title="Últimos 30 Registros",
                xaxis_title="Tempo",
                yaxis_title="Velocidade"
            )

            total = len(st.session_state.dados_reais)
            anomalias = (st.session_state.dados_reais['status'] == "Anômalo").sum()
            normais = (st.session_state.dados_reais['status'] == "Normal").sum()

            with placeholder.container():
                c1, c2 = st.columns([2, 1])
                c1.plotly_chart(fig, use_container_width=True)
                c2.metric("Total Registros", total)
                c2.metric("Normais", normais)
                c2.metric("Anomalias", anomalias)

            time.sleep(0.8)

    elif not st.session_state.dados_reais.empty:
        dados_plot = st.session_state.dados_reais.tail(30)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dados_plot["timestamp"],
            y=dados_plot["velocidade"],
            mode="lines",
            line=dict(color="royalblue"),
        ))
        color_map = dados_plot["status"].map({"Normal": "#1E90FF", "Anômalo": "#00CED1"}).tolist()
        fig.add_trace(go.Scatter(
            x=dados_plot["timestamp"],
            y=dados_plot["velocidade"],
            mode="markers",
            marker=dict(color=color_map, size=10),
        ))
        fig.add_hline(y=limite_inferior, line=dict(color="gray", dash="dash"))
        fig.add_hline(y=ideal, line=dict(color="black", dash="dot"))
        fig.add_hline(y=limite_superior, line=dict(color="gray", dash="dash"))
        placeholder.plotly_chart(fig, use_container_width=True)

# --------------------------
# 📊 Aba 2 — Estatísticas
# --------------------------
with tab2:
    st.header("Estatísticas Acumuladas")

    if len(st.session_state.dados_reais) > 0:
        dados = st.session_state.dados_reais.copy()
        media = dados['velocidade'].mean()
        desvio = dados['velocidade'].std()
        normais = (dados['status'] == "Normal").sum()
        anomalias = (dados['status'] == "Anômalo").sum()
        total = len(dados)
        pct_normais = (normais / total) * 100 if total > 0 else 0
        pct_anomalias = (anomalias / total) * 100 if total > 0 else 0

        st.markdown("""
        <style>
        .card {
            background: #2c2f38;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            height: 130px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .card h4 {
            color: white;
            font-size: 16px;
            margin-bottom: 10px;
        }
        .card h2 {
            font-size: 26px;
            margin: 0;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.markdown(f"""
        <div class="card">
            <h4>Média Velocidade</h4>
            <h2 style="color:#1E90FF;">{media:.4f}</h2>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="card">
            <h4>Desvio Padrão</h4>
            <h2 style="color:#00CED1;">{desvio:.4f}</h2>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div class="card">
            <h4>Total Registros</h4>
            <h2 style="color:#4FC3F7;">{total}</h2>
        </div>
        """, unsafe_allow_html=True)

        col4.markdown(f"""
        <div class="card">
            <h4>Percentual Normais</h4>
            <h2 style="color:#1E90FF;">{pct_normais:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)

        col5.markdown(f"""
        <div class="card">
            <h4>Percentual Anômalos</h4>
            <h2 style="color:#00CED1;">{pct_anomalias:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Distribuição das Velocidades")
        hist = px.histogram(
            dados, x="velocidade", color="status", nbins=20,
            barmode="overlay", color_discrete_map={"Normal": "#1E90FF", "Anômalo": "#00CED1"}
        )
        st.plotly_chart(hist, use_container_width=True)

        st.subheader("Proporção de Status")
        pie = px.pie(
            dados, names="status", hole=0.4,
            color="status", color_discrete_map={"Normal": "#1E90FF", "Anômalo": "#00CED1"}
        )
        st.plotly_chart(pie, use_container_width=True)
    else:
        st.info("Nenhum dado registrado ainda. Inicie a simulação na aba Tempo Real.")

# --------------------------
# 📄 Aba 3 — Sobre
# --------------------------
with tab3:
    st.header("Relatório Complementar (Vídeo)")

    video_path = "C:/Users/Cleo Leal/Downloads/geminicode-main/video/VideoAtuador.mp4"

    with open(video_path, "rb") as f:
        video_bytes = f.read()

    video_base64 = base64.b64encode(video_bytes).decode("utf-8")

    video_html = f"""
    <video id="meuVideo" width="800" height="450" controls autoplay loop muted>
      <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
      Seu navegador não suporta HTML5 video.
    </video>

    <script>
      var vid = document.getElementById('meuVideo');
      vid.playbackRate = 0.8;
    </script>
    """

    components.html(video_html, height=520)
