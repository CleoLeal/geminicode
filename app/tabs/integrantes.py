import streamlit as st
import os

def render():
    # --- CSS para fonte Poppins ---
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            html, body, [class*="css"] {
                font-family: 'Poppins', sans-serif !important;
                color: #e0e0e0;
            }
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Poppins', sans-serif !important;
                color: #416cd1;
            }
            .stMarkdown p, .stMarkdown a {
                font-family: 'Poppins', sans-serif !important;
                font-size: 15px;
                line-height: 1.6;
                color: #e0e0e0;
            }
            .stButton button {
                font-family: 'Poppins', sans-serif !important;
            }
        </style>
    """, unsafe_allow_html=True)

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

                st.markdown(f"<p style='text-align: left;'><b>{integrante['nome']}</b></p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: left;'><a href='{integrante['linkedin']}' target='_blank'>LinkedIn</a></p>", unsafe_allow_html=True)
    
    st.markdown("\n\n\n")
    
    st.header("Bibliografia")
    
    referencias = [
        {
            "titulo": "BionicKangaroo | Festo BR",
            "link": "https://www.festo.com/br/pt/e/sobre-a-festo/pesquisa-e-desenvolvimento/bionic-learning-network/robos-bionicos-ambulantes/bionickangaroo-id_33482/",
            "acesso": "4 out. 2025"
        },
        {
            "titulo": "Gêmeo digital e comissionamento virtual | Festo BR",
            "link": "https://www.festo.com/br/pt/e/solucoes/transformacao-digital/gemeo-digital-e-comissionamento-virtual-id_1643059/",
            "acesso": "4 out. 2025"
        },
        {
            "titulo": "Atuador normalizado DSNU-20-100-PPV-A | Festo BR",
            "link": "https://www.festo.com/br/pt/a/19239/?q=dsnu~%3AsortByCoreRangeAndNewProduct",
            "acesso": "4 out. 2025"
        },
        {
            "titulo": "Sensor de proximidade SME-8M-DS-24V-K-2,5-OE | Festo BR",
            "link": "https://www.festo.com/br/pt/a/543862/?q=SME+8M~%3AsortByCoreRangeAndNewProduct",
            "acesso": "4 out. 2025"
        },
        {
            "titulo": "Válvula solenoide VUVG-L10-B52-T-M5-1P3 | Festo BR",
            "link": "https://www.festo.com/br/pt/a/566458/?q=VUVG+L10+B52+T+M5+1P3~%3AfestoSortOrderScored",
            "acesso": "4 out. 2025"
        },
        {
            "titulo": "Digital twin | IBM",
            "link": "https://www.ibm.com/br-pt/think/topics/digital-twin",
            "acesso": "4 out. 2025"
        }
    ]
    
    for ref in referencias:
        st.markdown(f"- {ref['titulo']}. Disponível em: [link]({ref['link']}). Acesso em: {ref['acesso']}.")
