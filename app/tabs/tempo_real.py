#importações
import streamlit as st
import plotly.graph_objects as go
import time
from utils import gerar_dado
import config

# função principal da aba de monitoramento em tempo real
def render(df, le, model):
    # configurações iniciais
    st.header("Monitoramento em Tempo Real")

    #botões de controle
    col1, col2, col3 = st.columns([1, 1, 1])
    iniciar = col1.button("▶️ Iniciar Simulação")
    parar = col2.button("⏹️ Parar Simulação")
    resetar = col3.button("Resetar Histórico")

    # inicializa
    if iniciar:
        st.session_state.rodando = True
        st.session_state.aba_ativa = "tempo_real"
    # para
    if parar:
        st.session_state.rodando = False
        st.session_state.aba_ativa = "estatisticas"
    # reseta
    if resetar:
        st.session_state.dados_reais = st.session_state.dados_reais.iloc[0:0]

    # cria o dataframe vazio na sessão
    placeholder = st.empty()

    #deixar rodando "infinitamente"
    if st.session_state.rodando:
        for i in range(1000000):
            if not st.session_state.rodando:
                break
            # gera novo dado
            novo = gerar_dado(i, df, le, model,
                              config.IDEAL,
                              config.LIMITE_INFERIOR,
                              config.LIMITE_SUPERIOR,
                              st.session_state)
            # adiciona ao dataframe
            st.session_state.dados_reais = st.session_state.dados_reais._append(novo, ignore_index=True)
            dados_plot = st.session_state.dados_reais.tail(30)

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
                x=dados_plot[dados_plot["status"] == "Normal"]["timestamp"],
                y=dados_plot[dados_plot["status"] == "Normal"]["velocidade"],
                mode="markers",
                marker=dict(color="#416cd1", size=10),
                name="Normal"
            ))

            # markers anômalas
            fig.add_trace(go.Scatter(
                x=dados_plot[dados_plot["status"] == "Anômalo"]["timestamp"],
                y=dados_plot[dados_plot["status"] == "Anômalo"]["velocidade"],
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
            anomalias = (st.session_state.dados_reais['status'] == "Anômalo").sum()
            normais = (st.session_state.dados_reais['status'] == "Normal").sum()

            # exibe o gráfico e as métricas
            with placeholder.container():
                c1, c2 = st.columns([2, 1])
                c1.plotly_chart(fig, use_container_width=True)
                c2.metric("Total Registros", total)
                c2.metric("Normais", normais)
                c2.metric("Anomalias", anomalias)

            time.sleep(0.8)
            
    # exibe o gráfico estático quando não está rodando
    elif not st.session_state.dados_reais.empty:
        dados_plot = st.session_state.dados_reais.tail(30)
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dados_plot["timestamp"],
            y=dados_plot["velocidade"],
            mode="lines",
            line=dict(color="#787878"),
            line_shape="spline"
        ))

        fig.add_trace(go.Scatter(
            x=dados_plot[dados_plot["status"] == "Normal"]["timestamp"],
            y=dados_plot[dados_plot["status"] == "Normal"]["velocidade"],
            mode="markers",
            marker=dict(color="#416cd1", size=10),
            name="Normal"
        ))

        fig.add_trace(go.Scatter(
            x=dados_plot[dados_plot["status"] == "Anômalo"]["timestamp"],
            y=dados_plot[dados_plot["status"] == "Anômalo"]["velocidade"],
            mode="markers",
            marker=dict(color="#f1e500", size=10),
            name="Anômalo"
        ))

        fig.add_hline(y=config.LIMITE_INFERIOR, line=dict(color="gray", dash="dash"))
        fig.add_hline(y=config.IDEAL, line=dict(color="black", dash="dot"))
        fig.add_hline(y=config.LIMITE_SUPERIOR, line=dict(color="gray", dash="dash"))

        placeholder.plotly_chart(fig, use_container_width=True)
