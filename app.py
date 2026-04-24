import streamlit as st
import os
from datetime import datetime

# Configuração de página para ocupar o máximo de largura possível
st.set_page_config(page_title="Audit", layout="wide", initial_sidebar_state="collapsed")

# CSS AGRESSIVO: Reset de topo e layout de botões laterais
st.markdown("""
    <style>
    /* 1. Zerar o Topo Absolutamente */
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container {
        padding-top: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        margin-top: -45px !important; /* Puxa o conteúdo para o limite superior */
    }

    /* 2. Estética Deep Dark & Gold */
    html, body, [class*="css"] {
        background-color: #000000;
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }

    /* 3. Título Discreto */
    .header-label {
        font-size: 9px;
        letter-spacing: 3px;
        color: #444;
        text-transform: uppercase;
        margin-bottom: 10px;
        text-align: center;
    }

    /* 4. Imagem Controlada (Evita Scroll) */
    .stImage img {
        border: 1px solid #222;
        border-radius: 4px;
        max-height: 50vh !important; /* Imagem ocupa metade da altura da tela */
        width: auto;
        margin: 0 auto;
        display: block;
    }

    /* 5. Botões Laterais Estilizados */
    div.stButton > button {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid #1A1A1A !important;
        color: #555 !important;
        height: 50vh !important; /* Acompanha a altura da imagem */
        width: 100% !important;
        font-size: 30px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #D4AF37 !important;
        color: #D4AF37 !important;
        background-color: rgba(212, 175, 55, 0.05) !important;
    }

    /* 6. Caixa de Insight Moderna */
    .insight-card {
        background-color: #0A0A0A;
        padding: 15px 25px;
        border-top: 1px solid #1A1A1A;
        border-bottom: 2px solid #D4AF37;
        margin-top: 10px;
        font-size: 15px;
        line-height: 1.5;
        border-radius: 0 0 4px 4px;
    }

    /* Esconde o rodapé */
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

st.markdown('<p class="header-label">STRATEGY PROTOCOL // ESTUDO DE ABERTURAS</p>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("SISTEMA VAZIO // AGUARDANDO DADOS")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr_img = imgs[st.session_state.idx]
    p_img = os.path.join(IMG_DIR, curr_img)
    p_txt = p_img.replace(".jpg", ".txt")

    # LAYOUT DE 3 COLUNAS: [ BOTÃO ] [ IMAGEM ] [ BOTÃO ]
    c_prev, c_main, c_next = st.columns([1, 10, 1])
    
    with c_prev:
        st.write("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.rerun()

    with c_main:
        st.image(p_img, use_container_width=True)
        if os.path.exists(p_txt):
            with open(p_txt, "r") as f: texto = f.read()
            st.markdown(f'<div class="insight-card">{texto}</div>', unsafe_allow_html=True)

    with c_next:
        st.write("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.rerun()

    st.markdown(f"<p style='text-align:center; color:#222; font-size:9px; margin-top:15px;'>ENTRY {st.session_state.idx + 1} / {len(imgs)}</p>", unsafe_allow_html=True)

# GESTÃO (Final da página)
with st.expander("TERMINAL DE DADOS"):
    c1, c2 = st.columns(2)
    with c1:
        f = st.file_uploader("Novo Registro", type=["jpg", "png", "jpeg"])
        c = st.text_area("Análise:")
        if st.button("Salvar"):
            if f and c:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = os.path.join(IMG_DIR, f"{ts}.jpg")
                with open(path, "wb") as file: file.write(f.getbuffer())
                with open(path.replace(".jpg", ".txt"), "w") as file: file.write(c)
                st.rerun()
    with c2:
        if imgs:
            novo = st.text_area("Editar Atual:", value=texto if 'texto' in locals() else "")
            if st.button("Atualizar"):
                with open(p_txt, "w") as f: f.write(novo)
                st.rerun()
            if st.button("🗑️ Eliminar"):
                os.remove(p_img); os.remove(p_txt)
                st.session_state.idx = 0
                st.rerun()
