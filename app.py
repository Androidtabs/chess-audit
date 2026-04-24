import streamlit as st
import os
from datetime import datetime

# Configuração de Página: Amplitude Total
st.set_page_config(page_title="Chess Audit", layout="wide", initial_sidebar_state="collapsed")

# CSS: Design de Elite (Versão 2.0)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&family=Inter:wght@200;400;600&display=swap');

    /* Reset de UI Streamlit */
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        max-width: 1100px !important;
    }

    /* Fundo Profundo */
    html, body, [class*="css"] {
        background-color: #050505;
        color: #B0B0B0;
        font-family: 'Inter', sans-serif;
    }

    /* Barra de Título Técnica */
    .status-bar {
        border-bottom: 1px solid #1A1A1A;
        padding-bottom: 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .title-tag {
        font-size: 10px;
        letter-spacing: 3px;
        color: #D4AF37; /* Dourado */
        font-weight: 600;
        text-transform: uppercase;
    }

    /* O Dossier (Imagem) */
    .stImage {
        border: 1px solid #1A1A1A;
        border-radius: 4px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.8);
    }

    /* Container de Análise Profissional */
    .analysis-card {
        background: linear-gradient(145deg, #0A0A0A, #111111);
        border: 1px solid #1A1A1A;
        padding: 25px;
        border-radius: 4px;
        margin-top: 15px;
        position: relative;
    }
    .analysis-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: #555;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    .analysis-text {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        line-height: 1.7;
        color: #E0E0E0;
        font-weight: 400;
    }

    /* Botões de Navegação Estilo Interface de Controle */
    div.stButton > button {
        background-color: transparent !important;
        color: #333 !important;
        border: 1px solid #1A1A1A !important;
        height: 480px !important;
        width: 100% !important;
        font-size: 24px !important;
        transition: all 0.4s ease !important;
    }
    div.stButton > button:hover {
        border-color: #D4AF37 !important;
        color: #D4AF37 !important;
        box-shadow: inset 0 0 20px rgba(212, 175, 55, 0.05);
    }

    /* Expander de Gestão Elegante */
    .stExpander {
        border: none !important;
        background: transparent !important;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Status Bar Superior
st.markdown(f'''
    <div class="status-bar">
        <div class="title-tag">CHESS STRATEGY PROTOCOL // V 2.0</div>
        <div style="font-size: 10px; color: #444;">AUDIT_SESSION_{datetime.now().strftime("%Y%m%d")}</div>
    </div>
''', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("SISTEMA ONLINE // AGUARDANDO INPUT DE DADOS")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr_img = imgs[st.session_state.idx]
    p_img = os.path.join(IMG_DIR, curr_img)
    p_txt = p_img.replace(".jpg", ".txt")

    # Layout de Navegação Lateral
    c_ant, c_mid, c_prox = st.columns([0.4, 7, 0.4])
    
    with c_ant:
        st.write("<br>"*2, unsafe_allow_html=True)
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.rerun()

    with c_mid:
        st.image(p_img, use_container_width=True)
        if os.path.exists(p_txt):
            with open(p_txt, "r") as f: texto_analise = f.read()
            st.markdown(f'''
                <div class="analysis-card">
                    <div class="analysis-label">System Insight // Post-Game Analysis</div>
                    <div class="analysis-text">{texto_analise}</div>
                    <div style="position: absolute; right: 20px; bottom: 15px; font-size: 10px; color: #222;">DATA_REF: {curr_img[:8]}</div>
                </div>
            ''', unsafe_allow_html=True)

    with c_prox:
        st.write("<br>"*2, unsafe_allow_html=True)
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.rerun()

    st.markdown(f"<p style='text-align:center; color:#222; font-size:10px; letter-spacing:2px; margin-top:20px;'>RECORD {st.session_state.idx + 1} OF {len(imgs)}</p>", unsafe_allow_html=True)

# Gestão de Dados (Discreta)
with st.expander("TERMINAL DE GESTÃO DE ATIVOS"):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Ingestão de Dados")
        file = st.file_uploader("Upload Dossier", type=["jpg", "png", "jpeg"])
        insight = st.text_area("Insight Técnico:")
        if st.button("Confirmar Lançamento"):
            if file and insight:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = os.path.join(IMG_DIR, f"{ts}.jpg")
                with open(path, "wb") as f: f.write(file.getbuffer())
                with open(path.replace(".jpg", ".txt"), "w") as f: f.write(insight)
                st.rerun()
    with c2:
        if imgs:
            st.markdown("##### Modificação de Registro")
            edit_text = st.text_area("Corrigir Log:", value=texto_analise if 'texto_analise' in locals() else "")
            if st.button("Atualizar Banco de Dados"):
                with open(p_txt, "w") as f: f.write(edit_text)
                st.rerun()
            if st.button("Expurgar Registro"):
                os.remove(p_img); os.remove(p_txt)
                st.session_state.idx = 0
                st.rerun()
