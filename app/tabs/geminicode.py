import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# Caminho absoluto da pasta atual do script geminicode.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos para HTML e vídeo
HTML_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "html")
VIDEO_PATH = os.path.join(BASE_DIR, "..", "..", "assets", "VideoAtuador.mp4")

def render():
    st.header("Projeto GeminiCode")

    # --- HTML do projeto ---
    html_content = """
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
.section {
    margin-bottom: 40px;
    font-family: 'Poppins', sans-serif;
}
.section h2 {
    color: #416cd1ff;
    margin-bottom: 12px;
    font-size: 30px;
    font-weight: bold;
}
.section p {
    font-size: 20px;
    line-height: 1.7;
    color: #e0e0e0;
}
.card {
    background: #2c2f38;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
}
a {
    color: #f1e500ff;
    text-decoration: none;
    font-weight: bold;
}
a:hover {
    text-decoration: underline;
}
video {
    width: 100%;
    height: auto;
    max-height: 500px;
    border-radius: 15px;
}
</style>
<div class="section">
<h2>Contexto do Projeto</h2>
<div class="card">
<p>
Este projeto foi desenvolvido no âmbito da <b>Festo Innovation Challenge CUP 2025</b>,
uma iniciativa em parceria entre a <b>FIAP</b> e a <b>Festo</b>, com o objetivo de criar soluções
tecnológicas inovadoras voltadas ao <b>desenvolvimento de Digital Twins para monitoramento
de sistemas pneumáticos</b>.
</p>
<p>
A proposta buscou explorar o uso de <b>IoT, Inteligência Artificial, Machine Learning,
Visão Computacional</b> e a integração com sensores e atuadores industriais.  
O foco foi sempre em aplicações práticas, alinhadas à <b>Indústria 4.0</b> e
à <b>eficiência energética</b>.
</p>
</div>
</div>
<div class="section">
<h2>Demonstração do Protótipo</h2>
<video controls autoplay loop muted>
<source src="data:video/mp4;base64,VIDEO_BASE64" type="video/mp4">
Seu navegador não suporta vídeo.
</video>
</div>
"""

    # Substitui VIDEO_BASE64 pelo vídeo real
    with open(VIDEO_PATH, "rb") as f:
        video_bytes = f.read()
    video_base64 = base64.b64encode(video_bytes).decode("utf-8")
    final_html = html_content.replace("VIDEO_BASE64", video_base64)
    components.html(final_html, height=1000, scrolling=False)

    # Componentes utilizados
    st.subheader("Componentes Utilizados")

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

    # Impacto e Benefícios
    st.subheader("Impacto e Benefícios do Projeto")
    st.markdown("""<div style="font-size:20px; line-height:1.6;">  
        Nosso gêmeo digital traz vantagens significativas para a automação industrial, unindo confiabilidade operacional, eficiência energética e inteligência de dados:<br><br>
        ✅ Manutenção preditiva e redução de falhas — ao identificar padrões de funcionamento e prever possíveis anomalias, o sistema minimiza paradas não planejadas, aumenta a vida útil dos componentes e reduz custos com manutenção corretiva.<br><br>
        ✅ Eficiência energética otimizada — o monitoramento contínuo garante que o uso de ar comprimido seja feito de forma precisa e controlada, evitando desperdícios e contribuindo para práticas mais sustentáveis na indústria.<br><br>
        ✅ Integração físico-digital inteligente — a conexão entre sensores, atuadores e ambiente digital possibilita uma visão completa do processo em tempo real, permitindo ajustes rápidos e decisões baseadas em dados concretos.<br><br>
        ✅ Apoio estratégico à tomada de decisão — com dashboards interativos e intuitivos, gestores e operadores têm acesso a informações claras, facilitando a análise de desempenho e o planejamento de melhorias contínuas.<br><br>
        ✅ Escalabilidade e inovação — a solução pode ser expandida e adaptada a diferentes cenários industriais, mostrando o potencial da aplicação de gêmeos digitais como parte do futuro da Indústria 4.0.
        </div>
        """, unsafe_allow_html=True)
