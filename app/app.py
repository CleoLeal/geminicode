#importações
import streamlit as st
import config
from data_loader import carregar_dataset
from model import treinar_modelo
from tabs import tempo_real, estatisticas, geminicode

# config inicial
st.set_page_config(page_title=config.PAGE_TITLE, layout=config.LAYOUT)

# dataset e modelo
df = carregar_dataset()
model, le = treinar_modelo(df, config.LIMITE_INFERIOR, config.LIMITE_SUPERIOR)

# estado da sessão
if "dados_reais" not in st.session_state:
    st.session_state.dados_reais = df[["velocidade"]].head(0)  # vazio
if "rodando" not in st.session_state:
    st.session_state.rodando = False

# abas
tab1, tab2, tab3 = st.tabs(["Tempo Real", "Estatísticas", "GeminiCode"])

with tab1:
    tempo_real.render(df, le, model)

with tab2:
    estatisticas.render()

with tab3:
    geminicode.render()
