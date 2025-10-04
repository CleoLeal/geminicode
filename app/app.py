import streamlit as st
import config
from data_loader import carregar_dataset
from model import treinar_modelo
from tabs import tempo_real, estatisticas, geminicode, calculo, integrantes
import os

# Configuração inicial
st.set_page_config(page_title=config.PAGE_TITLE, layout=config.LAYOUT)

# Espaço antes da imagem
st.markdown("<div style='margin-top:45px;'></div>", unsafe_allow_html=True)

# Imagem fixa no header
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    logo_path = os.path.join(os.path.dirname(__file__), "image.png")
    st.image(logo_path, width=600)


# Dataset e modelo
df = carregar_dataset()
model, le = treinar_modelo(df, config.LIMITE_INFERIOR, config.LIMITE_SUPERIOR)

# Estado da sessão
if "dados_reais" not in st.session_state:
    st.session_state.dados_reais = df[["velocidade"]].head(0)  # vazio
if "rodando" not in st.session_state:
    st.session_state.rodando = False

# Abas
tab1, tab2, tab3, tab4, tab5 = st.tabs(["O que é o GeminiCode?", "Cálculos", "Simulação", "Resultados", "Integrantes e bibliografias"])

with tab1:
    geminicode.render()

with tab2:
    calculo.render()
    
with tab3:
    tempo_real.render(df, le, model)

with tab4:
    estatisticas.render()    

with tab5:
    integrantes.render()
