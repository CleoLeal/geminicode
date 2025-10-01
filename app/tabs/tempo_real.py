#importações
import streamlit as st
import plotly.graph_objects as go
import time
from utils import gerar_dado
import config
import pandas as pd

# função principal da aba de monitoramento em tempo real
def render(df, le, model):
    st.header("Monitoramento em Tempo Real")

    # botões de controle
    col1, col2, col3 = st.columns([1, 1, 1])
    iniciar = col1.button("▶️ Iniciar Simulação")
    parar = col2.button("⏹️ Parar Simulação")
    resetar = col3.button("Resetar Histórico")

    # inicializa
    if iniciar:
        st.session_state.rodando = True
        st.session_state.aba_ativa = "tempo_real"
    if parar:
        st.session_state.rodando = False
        st.session_state.aba_ativa = "estatisticas"
    if resetar:
        st.session_state.dados_reais = st.session_state.dados_reais.iloc[0:0]

    placeholder = st.empty()

    if st.session_state.rodando:
        for i in range(1000000):
            if not st.session_state.rodando:
                break

            # gera novo dado
            novo = gerar_dado(i, df, model, le, config.IDEAL, config.LIMITE_INFERIOR, config.LIMITE_SUPERIOR)
            st.session_state.dados_reais = pd.concat([st.session_state.dados_reais, pd.DataFrame([novo])], ignore_index=True)

            # pega últimos 30 registros para plot
            dados_plot = st.session_state.dados_reais.tail(30).copy()

            # define status apenas para plotagem baseado nos limites
            dados_plot['status_plot'] = dados_plot['velocidade'].apply(
                lambda x: "Normal" if config.LIMITE_INFERIOR <= x <= config.LIMITE_SUPERIOR else "Anômalo"
            )

            # cria o gráfico
            fig = go.Figure()

            # linha principal
            fig.add_trace(go.Scatter(
                x=dados_plot["timestamp"],
                y=dados_plot["velocidade"],
                mode="lines",
                line=dict(color="#787878", width=3),
                line_shape="spline"
            ))

            # markers normais
            fig.add_trace(go.Scatter(
                x=dados_plot[dados_plot["status_plot"] == "Normal"]["timestamp"],
                y=dados_plot[dados_plot["status_plot"] == "Normal"]["velocidade"],
                mode="markers",
                marker=dict(color="#416cd1", size=10),
                name="Normal"
            ))

            # markers anômalos
            fig.add_trace(go.Scatter(
                x=dados_plot[dados_plot["status_plot"] == "Anômalo"]["timestamp"],
                y=dados_plot[dados_plot["status_plot"] == "Anômalo"]["velocidade"],
                mode="markers",
                marker=dict(color="#f1e500", size=10),
                name="Anômalo"
            ))

            # linhas de referência
            fig.add_hline(y=config.LIMITE_INFERIOR, line=dict(color="gray", dash="dash"))
            fig.add_hline(y=config.IDEAL, line=dict(color="black", dash="dot"))
            fig.add_hline(y=config.LIMITE_SUPERIOR, line=dict(color="gray", dash="dash"))

            fig.update_layout(
                title="Últimos 30 Registros",
                xaxis_title="Tempo",
                yaxis_title="Velocidade"
            )

            # métricas
            total = len(st.session_state.dados_reais)
            anomalias = (st.session_state.dados_reais['velocidade'] < config.LIMITE_INFERIOR).sum() + \
                        (st.session_state.dados_reais['velocidade'] > config.LIMITE_SUPERIOR).sum()
            normais = total - anomalias

            # exibe o gráfico e métricas
            with placeholder.container():
                c1, c2 = st.columns([2, 1])
                c1.plotly_chart(fig, use_container_width=True)
                c2.metric("Total Registros", total)
                c2.metric("Normais", normais)
                c2.metric("Anomalias", anomalias)

            time.sleep(0.8)

    elif not st.session_state.dados_reais.empty:
        # gráfico estático quando não está rodando
        dados_plot = st.session_state.dados_reais.tail(30).copy()

        # define status apenas para plotagem
        dados_plot['status_plot'] = dados_plot['velocidade'].apply(
            lambda x: "Normal" if config.LIMITE_INFERIOR <= x <= config.LIMITE_SUPERIOR else "Anômalo"
        )

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dados_plot["timestamp"],
            y=dados_plot["velocidade"],
            mode="lines",
            line=dict(color="#787878"),
            line_shape="spline"
        ))

        fig.add_trace(go.Scatter(
            x=dados_plot[dados_plot["status_plot"] == "Normal"]["timestamp"],
            y=dados_plot[dados_plot["status_plot"] == "Normal"]["velocidade"],
            mode="markers",
            marker=dict(color="#416cd1", size=10),
            name="Normal"
        ))

        fig.add_trace(go.Scatter(
            x=dados_plot[dados_plot["status_plot"] == "Anômalo"]["timestamp"],
            y=dados_plot[dados_plot["status_plot"] == "Anômalo"]["velocidade"],
            mode="markers",
            marker=dict(color="#f1e500", size=10),
            name="Anômalo"
        ))

        fig.add_hline(y=config.LIMITE_INFERIOR, line=dict(color="gray", dash="dash"))
        fig.add_hline(y=config.IDEAL, line=dict(color="black", dash="dot"))
        fig.add_hline(y=config.LIMITE_SUPERIOR, line=dict(color="gray", dash="dash"))

        placeholder.plotly_chart(fig, use_container_width=True)
