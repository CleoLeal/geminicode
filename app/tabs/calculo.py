import streamlit as st
import plotly.express as px
import pandas as pd
import os

def render():
    st.header("Cálculos")

    # --- CSS para fonte Poppins ---
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            /* Aplica Poppins globalmente */
            html, body, [class*="css"]  {
                font-family: 'Poppins', sans-serif !important;
                color: #e0e0e0;
            }

            h1, h2, h3, h4, h5, h6 {
                font-family: 'Poppins', sans-serif !important;
                color: #416cd1;
            }

            .stMetric-value, .stMetric-label {
                font-family: 'Poppins', sans-serif !important;
            }

            .stMarkdown p {
                font-family: 'Poppins', sans-serif !important;
                font-size: 18px;
                line-height: 1.6;
            }

            .stButton button {
                font-family: 'Poppins', sans-serif !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- Introdução ---
    st.markdown("""
    O objetivo do nosso projeto é **validar se a velocidade do atuador está dentro do padrão esperado**
    ou se apresenta anomalias.
    """)

    col1, col2 = st.columns([2, 2])
    with col1:
        logo_path = os.path.join(os.path.dirname(__file__), "grafico_documentacao.png")
        st.image(logo_path, width=650)
    with col2:
        st.info("""
        🔹 Atuador analisado: **DSNU-20-100-PPV-A**  
        🔹 Velocidade máxima: **~1,4 m/s**  
        🔹 Distância entre sensores no ensaio: **8 cm**  
        """)

    # --- Resultados calculados ---
    velocidade_media = 0.057
    limite_inferior = 0.050
    limite_superior = 0.067

    st.subheader("Resultados dos cálculos")
    col1, col2, col3 = st.columns(3)
    col1.metric("Velocidade Média", f"{velocidade_media} m/s")
    col2.metric("Limite Inferior", f"{limite_inferior} m/s")
    col3.metric("Limite Superior", f"{limite_superior} m/s")

    st.markdown("""
    ✅ Consideramos uma margem de erro de 15%. Caso a velocidade se mantenha **dentro dos limites** mínimo e máximo estabelecidos, o atuador será classificado como **Normal**.  
    ⚠️ Caso contrário, será classificado como **Anômalo**.
    """)
    st.markdown("")
    st.markdown("---")
    # --- Dataset e Modelo ---
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Treinamento do modelo")
        st.write("""
        Para o treinamento foi utilizado um dataset contendo:  
        - Tipo de movimento (avanço/recuo)  
        - Tempo do movimento  
        - Velocidade média calculada  
        - Flag de anomalia (Normal/Anômalo)  

        O modelo escolhido foi o **RandomForestClassifier**, que obteve **100% de acurácia**.
        """)
    with col2:
        logo_path = os.path.join(os.path.dirname(__file__), "arvore_decisao.png")
        st.image(logo_path, width=800)

    st.markdown("")
    st.markdown("---")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(BASE_DIR,"dataset_velocidade_v2.xlsx")
    df = pd.read_excel(excel_path)

    if "Medição" not in df.columns:
        df["Medição"] = range(1, len(df) + 1)

    st.subheader("Histórico das velocidades")
    if df['flag'].dtype != object:  
        df['status'] = df['flag'].apply(lambda x: "Anômalo" if x == 0 else "Normal")
    else:  
        df['status'] = df['flag']

    fig = px.line(
        df,
        x="Medição",
        y="velocidade",
        markers=True,
        color="status",
        labels={"velocidade": "Velocidade (m/s)", "Medição": "Medição"}
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- Conclusão ---
    st.success("""
    O sistema está pronto para identificar anomalias em tempo real e auxiliar na validação do desempenho do atuador.
    """)
