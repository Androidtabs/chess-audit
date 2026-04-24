import streamlit as st
import os
from datetime import datetime

# 1. MANTENDO SUA CONFIGURAÇÃO ORIGINAL
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: SUA BASE FUNCIONAL + REFINAMENTO DE DESIGN
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    /* O SEU FIX DE TOPO (INALTERADO) */
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -30px !important;
        max-width: 1150px !important;
    }
    [data-testid="stAppViewContainer"] > section:nth-child(2) > div:nth-child(1) {
        padding-top: 0rem !important;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container {
        padding-top: 0rem !important;
    }

    /* ESTÉTICA DARK PREMIUM */
    html, body, [class*="css"] {
        background-color: #080808 !important;
        color: #E0E0E0 !important;
        font-family: 'Inter', sans-serif;
    }

    /* TÍTULO CENTRALIZADO */
    .header-text {
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        letter-spacing: 4px;
        color: #FFFFFF;
        margin-top: 0px !important;
        margin-bottom: 20px;
        font-size: 13px;
        text-transform: uppercase;
        text-align: center; /* CENTRALIZADO */
        opacity: 0.7;
    }

    /* IMAGEM DO TABULEIRO */
    img {
        max-height: 62vh !important;
        width: auto !important;
        margin: 0 auto;
        display: block;
        border-radius: 4px;
        border: 1px solid #1A1A1A;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }

    /* BOX DE ANÁLISE REFINADO */
    .insight-box {
        background-color: #0E0E0E;
        padding: 20px 40px;
        border-radius: 4px;
        border-bottom: 2px solid #D4AF37;
        font-size: 15px;
        color: #CCCCCC;
        margin-top: 15px;
        line-height: 1.6;
        text-align: center;
        max-width: 850px;
        margin-left: auto;
        margin-right: auto;
    }

    /* BOTÕES LATERAIS (MENORES E CENTRALIZADOS) */
    div.stButton > button {
        background-color: transparent !important;
        color: #444 !important;
        border: 1px solid #1A1A1A !important;
        height: 120px !important; /* REDUZIDO */
        width: 100% !important;
        font-size: 25px !important;
        transition: 0.3s ease;
        border-radius: 8px;
        margin-top: 180px; /* ALINHAMENTO VERTICAL AO CENTRO DO TABULEIRO */
    }
    
    div.stButton > button:hover {
        border-color: #D4AF37 !important;
        color: #D4AF37 !important;
        background-color: rgba(212, 175, 55, 0.05) !important;
    }

    /* LIMPEZA GERAL */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Título Centralizado
st.markdown('<p class="header-text">Chess Strategy Lab // Estudo de Aberturas</p>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("Aguardando input...")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    total = len(imgs)
    curr = imgs[st.session_state.idx]
    path_img = os.path.join(IMG_DIR, curr)
    path_txt = path_img.replace(".jpg", ".txt")

    # DISPLAY CENTRAL (MANTENDO SUAS PROPORÇÕES)
    c_ant, c_mid, c_prox = st.columns([0.6, 8, 0.6])
    
    with c_ant:
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % total
            st.rerun()

    with c_mid:
        st.image(path_img, use_container_width=True)
        if os.path.exists(path_txt):
            with open(path_txt, "r") as f: texto = f.read()
            st.markdown(f'<div class="insight-box"><b>ANÁLISE:</b> {texto}</div>', unsafe_allow_html=True)

    with c_prox:
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % total
            st.rerun()

    st.markdown(f"<p style='text-align:center; color:#111; font-size:10px; margin-top:15px;'>DATA_POINT {st.session_state.idx + 1} / {total}</p>", unsafe_allow_html=True)

# GESTÃO OCULTA (MANTIDA)
st.write("<br>"*2, unsafe_allow_html=True)
with st.expander("DADOS E PROPRIEDADES"):
    c1, c2 = st.columns(2)
    with c1:
        f = st.file_uploader("Novo Registro", type=["jpg", "png", "jpeg"])
        c = st.text_area("Insight da Engine:")
        if st.button("Salvar"):
            if f and c:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                p = os.path.join(IMG_DIR, f"{ts}.jpg")
                with open(p, "wb") as file: file.write(f.getbuffer())
                with open(p.replace(".jpg", ".txt"), "w") as file: file.write(c)
                st.rerun()
    with c2:
        if imgs:
            novo = st.text_area("Editar Texto:", value=texto if 'texto' in locals() else "")
            if st.button("Atualizar"):
                with open(path_txt, "w") as file: file.write(novo)
                st.rerun()
            if st.button("🗑️ Deletar"):
                os.remove(path_img); os.remove(path_txt)
                st.session_state.idx = 0
                st.rerun()
