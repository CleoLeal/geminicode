import streamlit as st
import config
from data_loader import carregar_dataset
from model import treinar_modelo
from tabs import tempo_real, estatisticas, geminicode, calculo, home

# Configuração inicial
st.set_page_config(page_title=config.PAGE_TITLE, layout=config.LAYOUT)

# --- Imagem fixa no header ---
col1, col2, col3 = st.columns([2, 2, 2])  # centraliza na coluna do meio
with col2:
    st.image("../assets/img/logo.png", width=800)

st.markdown("")
st.markdown("")
st.markdown("")



# Dataset e modelo
df = carregar_dataset()
model, le = treinar_modelo(df, config.LIMITE_INFERIOR, config.LIMITE_SUPERIOR)

# Estado da sessão
if "dados_reais" not in st.session_state:
    st.session_state.dados_reais = df[["velocidade"]].head(0)  # vazio
if "rodando" not in st.session_state:
    st.session_state.rodando = False

# Abas
tab1, tab2, tab3, tab4, tab5 = st.tabs(["O que é o GeminiCode?", "Simulação", "Resultados", "Cálculos", "Integrantes"])

with tab1:
    geminicode.render()

with tab2:
    tempo_real.render(df, le, model)

with tab3:
    estatisticas.render()

with tab4:
    calculo.render()

with tab5:
    home.render()
