import streamlit as st
import plotly.express as px
import config  

def render():
    st.header("Estatísticas Acumuladas")
    
    if len(st.session_state.dados_reais) > 0:
        dados = st.session_state.dados_reais.copy()
        
        # Define status para estatísticas baseado nos limites
        dados['status_calc'] = dados['velocidade'].apply(
            lambda x: "Normal" if config.LIMITE_INFERIOR <= x <= config.LIMITE_SUPERIOR else "Anômalo"
        )

        media = dados['velocidade'].mean()
        desvio = dados['velocidade'].std()
        normais = (dados['status_calc'] == "Normal").sum()
        anomalias = (dados['status_calc'] == "Anômalo").sum()
        total = len(dados)
        pct_normais = (normais / total) * 100 if total > 0 else 0
        pct_anomalias = (anomalias / total) * 100 if total > 0 else 0

        cards = [
            ("Média Velocidade", f"{media:.4f}", "#416cd1"),
            ("Desvio Padrão", f"{desvio:.4f}", "#f1e500"),
            ("Total Registros", f"{total}", "#4FC3F7"),
            ("Percentual Normais", f"{pct_normais:.1f}%", "#416cd1"),
            ("Percentual Anômalos", f"{pct_anomalias:.1f}%", "#f1e500")
        ]

        # Divide os cards em colunas (5 cards -> 5 colunas)
        cols = st.columns(len(cards))
        for col, (label, value, color) in zip(cols, cards):
            col.markdown(f"""
            <div style="
                background:#2c2f38;
                padding:20px;
                margin-bottom:12px;
                border-radius:15px;
                text-align:center;
            ">
                <div style="font-size:16px; color:#ffffff;">{label}</div>
                <div style="font-size:38px; color:{color}; font-weight:bold;">{value}</div>
            </div>
            """, unsafe_allow_html=True)

        # Histograma de velocidades
        st.subheader("Distribuição das Velocidades")
        hist = px.histogram(
            dados, x="velocidade", color="status_calc", nbins=20,
            barmode="overlay",
            color_discrete_map={"Normal": "#416cd1", "Anômalo": "#f1e500"}
        )
        st.plotly_chart(hist, use_container_width=True)

        # Pizza da proporção de status
        st.subheader("Proporção de Status")
        pie = px.pie(
            dados, names="status_calc", hole=0.4,
            color="status_calc",
            color_discrete_map={"Normal": "#416cd1", "Anômalo": "#f1e500"}
        )
        st.plotly_chart(pie, use_container_width=True)

    else:
        st.info("Nenhum dado registrado ainda. Inicie a simulação na aba Tempo Real.")
