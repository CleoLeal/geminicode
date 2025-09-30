#importações 
import streamlit as st
import plotly.express as px

# função para renderizar a aba de estatísticas
def render():
    st.header("Estatísticas Acumuladas")
    
    # verifica se há dados reais armazenados
    if len(st.session_state.dados_reais) > 0:
        dados = st.session_state.dados_reais.copy()
        media = dados['velocidade'].mean()
        desvio = dados['velocidade'].std()
        normais = (dados['status'] == "Normal").sum()
        anomalias = (dados['status'] == "Anômalo").sum()
        total = len(dados)
        pct_normais = (normais / total) * 100 if total > 0 else 0
        pct_anomalias = (anomalias / total) * 100 if total > 0 else 0

        col1, col2, col3, col4, col5 = st.columns(5)

        # Métricas com números grandes
        col1.markdown(f"""
        <div style="background:#2c2f38; padding:20px; border-radius:15px; text-align:center;">
            <div style="font-size:18px; color:#ffffff;">Média Velocidade</div>
            <div style="font-size:42px; color:#416cd1; font-weight:bold;">{media:.4f}</div>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div style="background:#2c2f38; padding:20px; border-radius:15px; text-align:center;">
            <div style="font-size:18px; color:#ffffff;">Desvio Padrão</div>
            <div style="font-size:42px; color:#f1e500; font-weight:bold;">{desvio:.4f}</div>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div style="background:#2c2f38; padding:20px; border-radius:15px; text-align:center;">
            <div style="font-size:18px; color:#ffffff;">Total Registros</div>
            <div style="font-size:42px; color:#4FC3F7; font-weight:bold;">{total}</div>
        </div>
        """, unsafe_allow_html=True)

        col4.markdown(f"""
        <div style="background:#2c2f38; padding:20px; border-radius:15px; text-align:center;">
            <div style="font-size:18px; color:#ffffff;">Percentual Normais</div>
            <div style="font-size:42px; color:#416cd1; font-weight:bold;">{pct_normais:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

        col5.markdown(f"""
        <div style="background:#2c2f38; padding:20px; border-radius:15px; text-align:center;">
            <div style="font-size:18px; color:#ffffff;">Percentual Anômalos</div>
            <div style="font-size:42px; color:#f1e500; font-weight:bold;">{pct_anomalias:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Distribuição das Velocidades")
        hist = px.histogram(
            dados, x="velocidade", color="status", nbins=20,
            barmode="overlay", color_discrete_map={"Normal": "#416cd1", "Anômalo": "#f1e500"}
        )
        st.plotly_chart(hist, use_container_width=True)

        st.subheader("Proporção de Status")
        pie = px.pie(
            dados, names="status", hole=0.4,
            color="status", color_discrete_map={"Normal": "#416cd1", "Anômalo": "#f1e500"}
        )
        st.plotly_chart(pie, use_container_width=True)
    else:
        st.info("Nenhum dado registrado ainda. Inicie a simulação na aba Tempo Real.")
