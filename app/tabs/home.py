import streamlit as st

def render():
    st.header("Equipe GeminiCode")
    st.markdown("Conheça os integrantes do nosso grupo:")

    integrantes = [
        {"nome": "Ana Julia Silva", "foto": "../assets/img/img_ana.png", "linkedin": "https://www.linkedin.com/in/ajuliaos/"},
        {"nome": "Cléo Leal", "foto": "../assets/img/img_cleo.png", "linkedin": "https://www.linkedin.com/in/cleovicttor/"},
        {"nome": "Letícia Wakai", "foto": "../assets/img/img_leticia.png", "linkedin": "https://www.linkedin.com/in/leticianaomiwakai/"},
        {"nome": "Murilo Lympius", "foto": "../assets/img/img_murilo.png", "linkedin": "https://www.linkedin.com/in/murilo-lympius/"},
        {"nome": "Renê Damasceno", "foto": "../assets/img/img_rene.png", "linkedin": "https://www.linkedin.com/in/renestachettidamasceno/"},
        {"nome": "Vitor Oliveira", "foto": "../assets/img/img_vitor.png", "linkedin": "https://www.linkedin.com/in/vitor-rodrigues-da-silva-oliveira-104013234/"},
    ]

    colunas_por_linha = 6  # 3 colunas no desktop

    for i in range(0, len(integrantes), colunas_por_linha):
        cols = st.columns(colunas_por_linha)
        for col, integrante in zip(cols, integrantes[i:i+colunas_por_linha]):
            with col:
                st.image(integrante["foto"], width=200)  # Imagem centralizada automaticamente na coluna
                st.markdown(f"<p style='text-align: left;'><b>{integrante['nome']}</b></p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: left;'><a href='{integrante['linkedin']}' target='_blank'>LinkedIn</a></p>", unsafe_allow_html=True)
                st.markdown(f"", unsafe_allow_html=True)
                st.markdown(f"", unsafe_allow_html=True)
                st.markdown(f"", unsafe_allow_html=True)
                st.markdown(f"", unsafe_allow_html=True)
