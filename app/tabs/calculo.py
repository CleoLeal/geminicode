import streamlit as st
import plotly.express as px
import pandas as pd
import os
def render():
    st.title("Cálculos")

    # --- Introdução ---
    st.markdown("""
    O objetivo do nosso projeto é **validar se a velocidade do atuador está dentro do padrão esperado**
    ou se apresenta anomalias.  
    """)
    col1, col2 = st.columns([2, 2])  # centraliza na coluna do meio
    with col1:
        logo_path = os.path.join(os.path.dirname(__file__), "grafico_documentacao.png")
        st.image(logo_path, width=500)
    with col2:
        st.info("""
        🔹 Atuador analisado: **DSNU-20-100-PPV-A**  
        🔹 Velocidade máxima: **~1,4 m/s**  
        🔹 Distância entre sensores no ensaio: **8 cm**  
        """)


    # --- Resultados calculados ---
    velocidade_media = 0.0571
    limite_inferior = velocidade_media * 0.95
    limite_superior = velocidade_media * 1.05

    st.subheader("Resultados dos Cálculos")
    col1, col2, col3 = st.columns(3)
    col1.metric("Velocidade Média", f"{velocidade_media:.4f} m/s")
    col2.metric("Limite Inferior", f"{limite_inferior:.4f} m/s")
    col3.metric("Limite Superior", f"{limite_superior:.4f} m/s")

    st.markdown("""
    ✅ Se a velocidade estiver **entre os limites mínimo e máximo**, o atuador é classificado como **Normal**.  
    ⚠️ Caso contrário, será classificado como **Anômalo**.
    """)

    # --- Dataset e Modelo ---
    st.subheader("Treinamento do Modelo")
    st.write("""
    Para o treinamento foi utilizado um dataset contendo:  
    - Tipo de movimento (avanço/recuo)  
    - Tempo do movimento  
    - Velocidade média calculada  
    - Flag de anomalia (Normal/Anômalo)  

    O modelo escolhido foi o **RandomForestClassifier**, que obteve **100% de acurácia**.
    """)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(BASE_DIR,"dataset_velocidade_v2.xlsx")
    df = pd.read_excel(excel_path)

    # Cria uma coluna de medição se não houver
    if "Medição" not in df.columns:
        df["Medição"] = range(1, len(df) + 1)

    st.subheader("Histórico das Velocidades")
    # Se a coluna flag estiver em 0/1 e você quiser converter para texto
    if df['flag'].dtype != object:  
        df['status'] = df['flag'].apply(lambda x: "Normal" if x == 0 else "Anômalo")
    else:  
        df['status'] = df['flag']  # já está em texto


    # Gráfico de linha com Plotly
    fig = px.line(
        df,
        x="Medição",
        y="velocidade",   # usa a coluna real do dataset
        title="Velocidade do Atuador ao Longo das Medições",
        markers=True,
        color="status",     # opcional: cor por normal/anomalia
        labels={"velocidade": "Velocidade (m/s)", "Medição": "Medição"}
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- Conclusão ---
    st.success("""
    O sistema está pronto para identificar anomalias em tempo real e auxiliar na validação do desempenho do atuador.  
    """)
