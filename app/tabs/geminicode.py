import streamlit as st
import streamlit.components.v1 as components
import os

# --- Caminhos absolutos ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "html")
GIF_PATH1 = os.path.join(BASE_DIR, "..", "..", "assets", "AtuadorGIF.gif")
GIF_PATH2 = os.path.join(BASE_DIR, "..", "..", "assets", "ColetandoDadosGIF.gif")

def render():
    st.header("Contexto")
    # --- CSS Global para responsividade ---
    st.markdown("""
    <style>
    /* Deixa o card ocupar toda a largura no celular */
    @media (max-width: 768px) {
        .card {
            width: 100% !important;
            margin: 0 !important;
            padding: 15px !important;
        }
        .section {
            padding: 0 !important;
        }
    }
    /* Remove espaços exagerados */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Texto antes do GIF ---
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
        .section {
            margin-bottom: 20px;
            font-family: 'Poppins', sans-serif;
        }
        .section h2 {
            color: #416cd1ff;
            margin-bottom: 12px;
            font-size: 30px;
            font-weight: bold;
        }
        .section p:first-child {
            font-size: 20px; /* novo tamanho */
            font-weight: 500; /* opcional */
        }
        .card {
            background: #2c2f38;
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
            overflow: visible;
            max-height: none;
        }
        a {
            color: #f1e500ff;
            text-decoration: none;
            font-weight: bold;
        }
        a:hover {
            text-decoration: underline;
        }
        </style>

        <div class="section">
            <div class="card">
                <p>
                Este projeto foi desenvolvido no âmbito da <b>Festo Innovation Challenge CUP 2025</b>,
                uma iniciativa em parceria entre a <b>FIAP</b> e a <b>Festo</b>, com o objetivo de criar soluções
                tecnológicas inovadoras voltadas ao <b>desenvolvimento de Digital Twins para monitoramento
                de sistemas pneumáticos</b>.<br>
                A proposta buscou explorar o uso de <b>IoT, Inteligência Artificial, Machine Learning,
                Visão Computacional</b> e a integração com sensores e atuadores industriais.  
                O foco foi sempre em aplicações práticas, alinhadas à <b>Indústria 4.0</b> e
                à <b>eficiência energética</b>.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)


    # --- GIFs ---
    col1, col2 = st.columns([2, 2]) 
    with col1:
        st.subheader("Demonstração do protótipo")
        st.image(GIF_PATH1, use_container_width=True)
    with col2:
        st.subheader("Coleta de dados")
        st.image(GIF_PATH2, use_container_width=True)

    # --- Componentes utilizados ---
    st.subheader("Componentes utilizados")

    # Atuador Normalizado
    col1, col2 = st.columns([1, 2])
    with col1:
        html_path = os.path.join(HTML_DIR, "AtuadorNormalizado.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=350, scrolling=False)
    with col2:
        st.markdown("""
        <h3>Atuador Normalizado — DSNU-20-100-PPV-A</h3>
        <div style="font-size:20px; line-height:1.6;">
            Cilindro pneumático de alta precisão utilizado para realizar o movimento linear.<br>
            É o principal componente físico monitorado pelo gêmeo digital.<br><br>
            <a href="https://www.festo.com/br/pt/a/19239/?q=dsnu%7E%3AsortByCoreRangeAndNewProduct" target="_blank">Mais detalhes</a>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

    # Sensor de Proximidade
    col1, col2 = st.columns([1, 2])
    with col1:
        html_path = os.path.join(HTML_DIR, "SensorProximidade.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=350, scrolling=False)
    with col2:
        st.markdown("""
        <h3>Sensor de Proximidade — SME-8M-DS-24V-K-2,5-OE</h3>
        <div style="font-size:20px; line-height:1.6;">
            Detecta a posição do êmbolo no interior do atuador, fornecendo feedback contínuo sobre o deslocamento.  
            Esses dados alimentam os algoritmos de <b>Machine Learning</b>, que distinguem estados normais e anômalos.<br><br>
            <a href="https://www.festo.com/br/pt/a/543862/?q=SME+8M%7E%3AsortByCoreRangeAndNewProduct" target="_blank">Mais detalhes</a>  
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

    # Válvula Solenoide
    col1, col2 = st.columns([1, 2])
    with col1:
        html_path = os.path.join(HTML_DIR, "ValvulaSolenoide.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=350, scrolling=False)
    with col2:
        st.markdown("""
        <h3>Válvula Solenoide — VUVG-L10-B52-T-M5-1P3</h3>
        <div style="font-size:20px; line-height:1.6;"> 
        Responsável pelo controle preciso do fluxo de ar comprimido que aciona o atuador.  
        Seu papel é garantir que os movimentos sejam realizados com exatidão, integrando-se ao sistema de monitoramento digital. <br><br>
            <a href="https://www.festo.com/br/pt/a/566458/?q=VUVG+L10+B52+T+M5+1P3%7E%3AfestoSortOrderScored" target="_blank">Mais detalhes</a>  
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

        # --- Aplicação da família DSNU + Vídeo ---
    st.markdown("## Aplicação da família de atuadores DSNU")

    col1, col2 = st.columns([2, 2])  # duas colunas lado a lado
    with col1:
        VIDEO_PATH = os.path.join(BASE_DIR, "..", "..", "assets", "BionicKangaroo.mp4")
        if os.path.exists(VIDEO_PATH):
            st.video(VIDEO_PATH)
        else:
            st.info("📹 Vídeo demonstrativo do atuador DSNU em breve...")
        
    st.markdown("")
    st.markdown("---")


    with col2:
        st.markdown("""
        <div style="font-size:20px; line-height:1.7; font-family:'Poppins', sans-serif; color:#e0e0e0; text-align:justify;">
        O Atuador Normalizado DSNU-20-100-PPV-A, presente em nosso protótipo, integra a linha de cilindros pneumáticos DSNU da Festo, reconhecida pela robustez e precisão. Embora não seja o mesmo modelo do projeto BionicKangaroo, ambos pertencem a essa família. 
        <br>No robô, o DSNU foi fundamental para os saltos suaves e controlados do canguru; já no Projeto GeminiCode, atua como “músculo” do sistema, realizando o movimento linear monitorado pelo gêmeo digital. Essa versatilidade mostra como a linha DSNU atende desde aplicações industriais até soluções inovadoras inspiradas na natureza.
        </div>
        """, unsafe_allow_html=True)

    # Impacto e Benefícios
    st.markdown("""
    <style>
        .benefits-container {
            background-color: #2c2f38;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
            font-family: 'Poppins', sans-serif;
            color: #e0e0e0;
            margin-bottom: 20px;
        }
        .benefits-container h3 {
            color: #f1e500;
            font-size: 26px;
            margin-bottom: 15px;
        }
        .benefits-container p {
            font-size: 20px;
            line-height: 1.7;
        }
        .benefits-container ul {
            padding-left: 20px;
            font-size: 20px;
            line-height: 1.7;
        }
        .benefits-container li {
            margin-bottom: 15px;
        }
    </style>

    <div class="benefits-container">
        <h3>Impacto e benefícios do projeto</h3>
        <p>
        Nosso gêmeo digital impulsiona a automação industrial com <b>confiabilidade</b>, <b>eficiência</b> e <b>inteligência de dados</b>.
        </p>
        <ul>
            <li><b>Manutenção preditiva</b> – Antecipação de falhas, menos paradas e maior vida útil dos componentes.</li>
            <li><b>Eficiência energética</b> – Uso racional do ar comprimido e redução de desperdícios.</li>
            <li><b>Integração físico-digital</b> – Monitoramento em tempo real e decisões baseadas em dados.</li>
            <li><b>Suporte estratégico</b> – Dashboards interativos para análises rápidas e precisas.</li>
            <li><b>Escalabilidade</b> – Flexível para diferentes aplicações na Indústria 4.0.</li>
        </ul>
    </div>

    """, unsafe_allow_html=True)

