import streamlit as st
import os

def render():
    st.header("Equipe GeminiCode")
    st.markdown("Conheça os integrantes do nosso grupo:")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pasta onde o script está

    integrantes = [
        {"nome": "Ana Julia Silva", "foto": "img_ana.png", "linkedin": "https://www.linkedin.com/in/ajuliaos/"},
        {"nome": "Cléo Leal", "foto": "img_cleo.png", "linkedin": "https://www.linkedin.com/in/cleovicttor/"},
        {"nome": "Letícia Wakai", "foto": "img_leticia.png", "linkedin": "https://www.linkedin.com/in/leticianaomiwakai/"},
        {"nome": "Murilo Lympius", "foto": "img_murilo.png", "linkedin": "https://www.linkedin.com/in/murilo-lympius/"},
        {"nome": "Renê Damasceno", "foto": "img_rene.png", "linkedin": "https://www.linkedin.com/in/renestachettidamasceno/"},
        {"nome": "Vitor Oliveira", "foto": "img_vitor.png", "linkedin": "https://www.linkedin.com/in/vitor-rodrigues-da-silva-oliveira-104013234/"},
    ]

    colunas_por_linha = 6  # quantidade de colunas por linha

    for i in range(0, len(integrantes), colunas_por_linha):
        cols = st.columns(colunas_por_linha)
        for col, integrante in zip(cols, integrantes[i:i+colunas_por_linha]):
            with col:
                # Cria o caminho completo da imagem
                foto_path = os.path.join(BASE_DIR, integrante["foto"])
                
                if os.path.exists(foto_path):
                    st.image(foto_path, width=200)
                else:
                    st.warning(f"Imagem não encontrada: {foto_path}")

                st.markdown(f"<p style='text-align: center;'><b>{integrante['nome']}</b></p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center;'><a href='{integrante['linkedin']}' target='_blank'>LinkedIn</a></p>", unsafe_allow_html=True)
